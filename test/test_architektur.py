"""Architektur-Tests: erzwingen die DDD-Struktur automatisch (lokal und in der CI).

Regeln:
 R1  Ein Bounded Context importiert nie einen anderen Bounded Context.
 R2  Die Domäne importiert weder Application noch Infrastructure.
 R3  Die Application-Schicht importiert nicht die Infrastructure-Schicht.
 R4  Domäne und Application nutzen keine Frameworks (FastAPI, SQLAlchemy, Pydantic ...).
"""
import ast
from pathlib import Path

import pytest

PROJEKTWURZEL = Path(__file__).resolve().parent.parent
PAKET = "meditrack"
PAKETPFAD = PROJEKTWURZEL / PAKET
SCHICHTEN = ("domain", "application", "infrastructure")
FRAMEWORKS = {"fastapi", "starlette", "uvicorn", "sqlalchemy", "pydantic"}


def _kontexte() -> list[str]:
    return sorted(
        ordner.name for ordner in PAKETPFAD.iterdir()
        if ordner.is_dir() and (ordner / "__init__.py").exists()
    )


def _module() -> list[Path]:
    return sorted(
        datei for datei in PAKETPFAD.rglob("*.py")
        if "__pycache__" not in datei.parts and datei.name != "__init__.py"
    )


def _modulteile(datei: Path) -> list[str]:
    """meditrack/a/domain/model.py -> ['meditrack', 'a', 'domain', 'model']"""
    return list(datei.relative_to(PROJEKTWURZEL).with_suffix("").parts)


def importierte_module(modulteile: list[str], quelltext: str) -> list[str]:
    """Liefert alle importierten Module als absolute, gepunktete Namen (relative Importe aufgelöst)."""
    paket = modulteile[:-1]
    ergebnis: list[str] = []

    for knoten in ast.walk(ast.parse(quelltext)):
        if isinstance(knoten, ast.Import):
            ergebnis.extend(alias.name for alias in knoten.names)
        elif isinstance(knoten, ast.ImportFrom):
            if knoten.level == 0:
                basis = knoten.module.split(".") if knoten.module else []
            else:
                ausgangspunkt = paket[: len(paket) - (knoten.level - 1)]
                basis = ausgangspunkt + (knoten.module.split(".") if knoten.module else [])
            ergebnis.append(".".join(basis))

    return ergebnis


def verletzungen(modulteile: list[str], importe: list[str], kontexte: list[str]) -> list[str]:
    """Prüft die Regeln R1-R4 für ein Modul und liefert die Verstöße als Text."""
    if len(modulteile) < 3:
        return []

    kontext, schicht = modulteile[1], modulteile[2]
    gefunden = []

    for ziel in importe:
        teile = ziel.split(".")

        if teile[0] in FRAMEWORKS and schicht in ("domain", "application"):
            gefunden.append(f"R4: {schicht} importiert Framework '{ziel}'")

        if teile[0] != PAKET or len(teile) < 2:
            continue

        ziel_kontext = teile[1]
        ziel_schicht = teile[2] if len(teile) > 2 else None

        if ziel_kontext in kontexte and ziel_kontext != kontext:
            gefunden.append(f"R1: {kontext} importiert fremden Context '{ziel}'")
        elif schicht == "domain" and ziel_schicht in ("application", "infrastructure"):
            gefunden.append(f"R2: domain importiert {ziel_schicht} ('{ziel}')")
        elif schicht == "application" and ziel_schicht == "infrastructure":
            gefunden.append(f"R3: application importiert infrastructure ('{ziel}')")

    return gefunden


# Die tatsächliche Projektstruktur muss den Regeln entsprechen

@pytest.mark.parametrize("datei", _module(), ids=lambda d: d.relative_to(PROJEKTWURZEL).as_posix())
def test_modul_haelt_architekturregeln_ein(datei):
    importe = importierte_module(_modulteile(datei), datei.read_text(encoding="utf-8"))

    assert verletzungen(_modulteile(datei), importe, _kontexte()) == []


@pytest.mark.parametrize("kontext", _kontexte())
def test_jeder_kontext_hat_alle_drei_schichten(kontext):
    for schicht in SCHICHTEN:
        ordner = PAKETPFAD / kontext / schicht

        assert ordner.is_dir(), f"{kontext}: Schicht '{schicht}' fehlt"
        assert (ordner / "__init__.py").exists(), f"{kontext}/{schicht}: __init__.py fehlt"


def test_alle_erwarteten_bounded_contexts_sind_vorhanden():
    assert _kontexte() == [
        "alarmmanagement",
        "behandlungsdokumentation",
        "benutzerverwaltung",
        "patientenverwaltung",
        "vitaldatenueberwachung",
    ]


# Der Prüfer selbst: erkennt er echte Verstöße? (sonst wären die Tests oben wirkungslos)

KONTEXTE = ["alarmmanagement", "patientenverwaltung"]
MODUL_DOMAIN = ["meditrack", "alarmmanagement", "domain", "model"]
MODUL_APPLICATION = ["meditrack", "alarmmanagement", "application", "alarm_service"]


def test_relative_importe_werden_aufgeloest():
    quelle = "from ..domain.model import X\nfrom .helfer import Y\nfrom ...patientenverwaltung.domain import Z"

    assert importierte_module(MODUL_APPLICATION, quelle) == [
        "meditrack.alarmmanagement.domain.model",
        "meditrack.alarmmanagement.application.helfer",
        "meditrack.patientenverwaltung.domain",
    ]


def test_import_eines_fremden_contexts_wird_erkannt():
    importe = importierte_module(MODUL_DOMAIN, "from meditrack.patientenverwaltung.domain.model import Patient")

    assert any(v.startswith("R1") for v in verletzungen(MODUL_DOMAIN, importe, KONTEXTE))


def test_relativer_import_in_fremden_context_wird_erkannt():
    importe = importierte_module(MODUL_APPLICATION, "from ...patientenverwaltung.domain.model import Patient")

    assert any(v.startswith("R1") for v in verletzungen(MODUL_APPLICATION, importe, KONTEXTE))


def test_domain_darf_infrastructure_nicht_importieren():
    importe = importierte_module(MODUL_DOMAIN, "from ..infrastructure.in_memory_repositories import R")

    assert any(v.startswith("R2") for v in verletzungen(MODUL_DOMAIN, importe, KONTEXTE))


def test_application_darf_infrastructure_nicht_importieren():
    importe = importierte_module(MODUL_APPLICATION, "from ..infrastructure.in_memory_repositories import R")

    assert any(v.startswith("R3") for v in verletzungen(MODUL_APPLICATION, importe, KONTEXTE))


@pytest.mark.parametrize("quelle", ["import sqlalchemy", "from fastapi import FastAPI", "from pydantic import BaseModel"])
def test_frameworks_in_der_domain_werden_erkannt(quelle):
    importe = importierte_module(MODUL_DOMAIN, quelle)

    assert any(v.startswith("R4") for v in verletzungen(MODUL_DOMAIN, importe, KONTEXTE))


def test_erlaubte_importe_ergeben_keine_verstoesse():
    quelle = (
        "from dataclasses import dataclass\n"
        "from uuid import UUID\n"
        "from ..domain.model import Warnmeldung\n"
        "from ..domain.repositories import WarnmeldungRepository\n"
    )
    importe = importierte_module(MODUL_APPLICATION, quelle)

    assert verletzungen(MODUL_APPLICATION, importe, KONTEXTE) == []


def test_infrastructure_darf_domain_importieren():
    modul = ["meditrack", "alarmmanagement", "infrastructure", "in_memory_repositories"]
    importe = importierte_module(modul, "from ..domain.model import Warnmeldung")

    assert verletzungen(modul, importe, KONTEXTE) == []
