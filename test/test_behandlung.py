from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from meditrack.behandlungsdokumentation.application.behandlungs_service import (
    BehandlungsService,
)
from meditrack.behandlungsdokumentation.domain.model import Behandlung
from meditrack.behandlungsdokumentation.infrastructure.in_memory_repositories import (
    InMemoryBehandlungsRepository,
)


def _behandlung(**ueberschreibungen):
    parameter = {
        "behandlung_id": uuid4(),
        "patient_id": uuid4(),
        "mitarbeiter_id": uuid4(),
        "massnahme": "Medikamentengabe",
        "zeitpunkt": datetime.now(),
    }
    parameter.update(ueberschreibungen)
    return Behandlung(**parameter)


# Happy-Path-Tests

def test_gueltige_behandlung():
    patient_id, mitarbeiter_id = uuid4(), uuid4()

    behandlung = _behandlung(patient_id=patient_id, mitarbeiter_id=mitarbeiter_id)

    assert behandlung.patient_id == patient_id
    assert behandlung.mitarbeiter_id == mitarbeiter_id
    assert behandlung.massnahme == "Medikamentengabe"
    assert behandlung.notiz == ""


def test_behandlung_mit_notiz():
    behandlung = _behandlung(notiz="Patient verträgt das Medikament gut")

    assert behandlung.notiz == "Patient verträgt das Medikament gut"


# Negative Tests

@pytest.mark.parametrize("feld", ["behandlung_id", "patient_id", "mitarbeiter_id"])
@pytest.mark.parametrize("wert", [None, "kein-uuid", 42])
def test_ungueltige_ids(feld, wert):
    with pytest.raises(ValueError):
        _behandlung(**{feld: wert})


@pytest.mark.parametrize("massnahme", ["", "   ", "\t\n", None, 42])
def test_ungueltige_massnahme(massnahme):
    with pytest.raises(ValueError):
        _behandlung(massnahme=massnahme)


@pytest.mark.parametrize("zeitpunkt", [None, "2026-01-01", 1234567890])
def test_ungueltiger_zeitpunkt(zeitpunkt):
    with pytest.raises(ValueError):
        _behandlung(zeitpunkt=zeitpunkt)


@pytest.mark.parametrize("notiz", [None, 42])
def test_notiz_muss_text_sein(notiz):
    with pytest.raises(ValueError):
        _behandlung(notiz=notiz)


# Edge-Cases

def test_zeitpunkt_in_der_zukunft_wird_abgelehnt():
    with pytest.raises(ValueError):
        _behandlung(zeitpunkt=datetime.now() + timedelta(days=1))


def test_zeitpunkt_mit_zeitzone_wird_akzeptiert():
    behandlung = _behandlung(zeitpunkt=datetime.now(timezone.utc))

    assert behandlung.zeitpunkt.tzinfo is not None


def test_zeitpunkt_mit_zeitzone_in_der_zukunft_wird_abgelehnt():
    with pytest.raises(ValueError):
        _behandlung(zeitpunkt=datetime.now(timezone.utc) + timedelta(hours=1))


def test_massnahme_mit_umlauten_und_sonderzeichen():
    assert _behandlung(massnahme="Verbandwechsel (Bein, links) – 2×").massnahme.startswith("Verband")


def test_patient_und_mitarbeiter_duerfen_dieselbe_id_nicht_teilen():
    gemeinsame_id = uuid4()

    with pytest.raises(ValueError):
        _behandlung(patient_id=gemeinsame_id, mitarbeiter_id=gemeinsame_id)


def test_behandlung_ist_unveraenderlich():
    behandlung = _behandlung()

    with pytest.raises(AttributeError):
        behandlung.massnahme = "Anderes"


# Application Service + Repository

def test_behandlung_dokumentieren_speichert_sie():
    repository = InMemoryBehandlungsRepository()
    service = BehandlungsService(repository)
    patient_id, mitarbeiter_id = uuid4(), uuid4()

    behandlung = service.behandlung_dokumentieren(
        patient_id=patient_id,
        mitarbeiter_id=mitarbeiter_id,
        massnahme="Infusion angelegt",
        notiz="Linker Arm",
    )

    assert behandlung.massnahme == "Infusion angelegt"
    assert behandlung.notiz == "Linker Arm"
    assert repository.finde_nach_patient(patient_id) == [behandlung]


def test_zeitpunkt_wird_standardmaessig_auf_jetzt_gesetzt():
    service = BehandlungsService(InMemoryBehandlungsRepository())
    vorher = datetime.now()

    behandlung = service.behandlung_dokumentieren(uuid4(), uuid4(), "Blutdruck gemessen")

    assert vorher <= behandlung.zeitpunkt <= datetime.now()


def test_ungueltige_behandlung_wird_nicht_gespeichert():
    repository = InMemoryBehandlungsRepository()
    service = BehandlungsService(repository)

    with pytest.raises(ValueError):
        service.behandlung_dokumentieren(uuid4(), uuid4(), "   ")

    assert repository.behandlungen == {}


def test_verlauf_ist_nach_zeitpunkt_sortiert():
    service = BehandlungsService(InMemoryBehandlungsRepository())
    patient_id, mitarbeiter_id = uuid4(), uuid4()
    jetzt = datetime.now()

    spaet = service.behandlung_dokumentieren(patient_id, mitarbeiter_id, "Entlassungsgespräch", jetzt)
    frueh = service.behandlung_dokumentieren(
        patient_id, mitarbeiter_id, "Aufnahme", jetzt - timedelta(days=2)
    )
    mitte = service.behandlung_dokumentieren(
        patient_id, mitarbeiter_id, "Operation", jetzt - timedelta(days=1)
    )

    assert service.verlauf_abrufen(patient_id) == [frueh, mitte, spaet]


def test_verlauf_enthaelt_nur_behandlungen_des_patienten():
    service = BehandlungsService(InMemoryBehandlungsRepository())
    patient_a, patient_b, mitarbeiter_id = uuid4(), uuid4(), uuid4()

    eigene = service.behandlung_dokumentieren(patient_a, mitarbeiter_id, "Aufnahme")
    service.behandlung_dokumentieren(patient_b, mitarbeiter_id, "Aufnahme")

    assert service.verlauf_abrufen(patient_a) == [eigene]


def test_verlauf_ohne_behandlungen_ist_leer():
    assert BehandlungsService(InMemoryBehandlungsRepository()).verlauf_abrufen(uuid4()) == []


def test_verlauf_ist_eine_kopie_und_aendert_das_repository_nicht():
    repository = InMemoryBehandlungsRepository()
    service = BehandlungsService(repository)
    patient_id = uuid4()
    service.behandlung_dokumentieren(patient_id, uuid4(), "Aufnahme")

    service.verlauf_abrufen(patient_id).clear()

    assert len(service.verlauf_abrufen(patient_id)) == 1


def test_gleiche_massnahme_zweimal_ergibt_zwei_eintraege():
    service = BehandlungsService(InMemoryBehandlungsRepository())
    patient_id, mitarbeiter_id = uuid4(), uuid4()

    service.behandlung_dokumentieren(patient_id, mitarbeiter_id, "Medikamentengabe")
    service.behandlung_dokumentieren(patient_id, mitarbeiter_id, "Medikamentengabe")

    assert len(service.verlauf_abrufen(patient_id)) == 2
