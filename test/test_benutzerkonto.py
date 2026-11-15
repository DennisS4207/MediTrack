from uuid import uuid4

import pytest

from meditrack.benutzerverwaltung.application.registrierungs_service import (
    RegistrierungsService,
)
from meditrack.benutzerverwaltung.domain.model import Benutzerkonto, Benutzerrolle
from meditrack.benutzerverwaltung.infrastructure.in_memory_repositories import (
    InMemoryBenutzerRepository,
)

# Happy-Path-Tests


def test_gueltiges_benutzerkonto():
    konto = Benutzerkonto(
        benutzer_id=uuid4(),
        email="max@example.com",
        passwort_hash="gesicherter_hash",
        rolle=Benutzerrolle.PATIENT
    )

    assert konto.email == "max@example.com"
    assert konto.rolle == "PATIENT"
    assert konto.ist_patient is True


def test_mitarbeiterkonto():
    konto = Benutzerkonto(
        benutzer_id=uuid4(),
        email="arzt@example.com",
        passwort_hash="gesicherter_hash",
        rolle=Benutzerrolle.MITARBEITER
    )

    assert konto.rolle == "MITARBEITER"
    assert konto.ist_patient is False


# Negative Tests

def test_leere_email():
    with pytest.raises(ValueError):
        Benutzerkonto(uuid4(), "", "hash", Benutzerrolle.PATIENT)


def test_ungueltige_email():
    with pytest.raises(ValueError):
        Benutzerkonto(uuid4(), "ungueltige-email", "hash", Benutzerrolle.PATIENT)


def test_leerer_passwort_hash():
    with pytest.raises(ValueError):
        Benutzerkonto(uuid4(), "max@example.com", "", Benutzerrolle.PATIENT)


def test_ungueltige_rolle():
    with pytest.raises(ValueError):
        Benutzerkonto(uuid4(), "max@example.com", "hash", "ADMIN")


# Edge-Cases

def test_email_mit_pluszeichen():
    konto = Benutzerkonto(uuid4(), "max+test@example.com", "hash", "PATIENT")

    assert konto.email == "max+test@example.com"


def test_fehlende_benutzer_id():
    with pytest.raises(ValueError):
        Benutzerkonto(None, "max@example.com", "hash", Benutzerrolle.PATIENT)


def test_rolle_als_text_wird_in_enum_umgewandelt():
    konto = Benutzerkonto(uuid4(), "max@example.com", "hash", "MITARBEITER")

    assert konto.rolle is Benutzerrolle.MITARBEITER


@pytest.mark.parametrize("rolle", [None, "", "patient", 1])
def test_unzulaessige_rollen(rolle):
    with pytest.raises(ValueError):
        Benutzerkonto(uuid4(), "max@example.com", "hash", rolle)


@pytest.mark.parametrize(
    "email",
    [
        None,
        123,
        " max@example.com",
        "max@example.com ",
        "max@example.com\n",
        "max @example.com",
        "max@@example.com",
        "@example.com",
        "max@",
        "max@example",
        "max@example.c",
    ],
)
def test_ungueltige_email_formate(email):
    with pytest.raises(ValueError):
        Benutzerkonto(uuid4(), email, "hash", Benutzerrolle.PATIENT)


@pytest.mark.parametrize(
    "email",
    ["a@b.de", "vor.name@sub.example.co.uk", "max_mustermann@example.org"],
)
def test_gueltige_email_formate(email):
    assert Benutzerkonto(uuid4(), email, "hash", Benutzerrolle.PATIENT).email == email


@pytest.mark.parametrize("passwort_hash", [None, "   ", 123])
def test_unzulaessiger_passwort_hash(passwort_hash):
    with pytest.raises(ValueError):
        Benutzerkonto(uuid4(), "max@example.com", passwort_hash, Benutzerrolle.PATIENT)


def test_passwort_hash_taucht_nicht_in_repr_auf():
    konto = Benutzerkonto(uuid4(), "max@example.com", "geheimer_hash", Benutzerrolle.PATIENT)

    assert "geheimer_hash" not in repr(konto)


def test_benutzerkonto_ist_unveraenderlich():
    konto = Benutzerkonto(uuid4(), "max@example.com", "hash", Benutzerrolle.PATIENT)

    with pytest.raises(AttributeError):
        konto.email = "neu@example.com"


# Application Service + Repository

def test_erfolgreiche_registrierung():
    repository = InMemoryBenutzerRepository()
    service = RegistrierungsService(repository)

    konto = service.registrieren(
        email="anna@example.com",
        passwort_hash="gesicherter_hash",
        rolle="PATIENT"
    )

    assert konto.email == "anna@example.com"
    assert konto.rolle == "PATIENT"
    assert repository.finde_nach_email("anna@example.com") == konto


def test_doppelte_email_verhindern():
    repository = InMemoryBenutzerRepository()
    service = RegistrierungsService(repository)

    service.registrieren(
        email="anna@example.com",
        passwort_hash="gesicherter_hash",
        rolle="PATIENT"
    )

    with pytest.raises(ValueError):
        service.registrieren(
            email="anna@example.com",
            passwort_hash="anderer_hash",
            rolle="PATIENT"
        )


def test_doppelte_email_ignoriert_gross_und_kleinschreibung():
    service = RegistrierungsService(InMemoryBenutzerRepository())
    service.registrieren("anna@example.com", "hash", "PATIENT")

    with pytest.raises(ValueError):
        service.registrieren("Anna@Example.COM", "hash", "MITARBEITER")


def test_registrierung_mit_ungueltiger_email():
    repository = InMemoryBenutzerRepository()
    service = RegistrierungsService(repository)

    with pytest.raises(ValueError):
        service.registrieren(
            email="ungueltig",
            passwort_hash="gesicherter_hash",
            rolle="PATIENT"
        )


def test_fehlgeschlagene_registrierung_speichert_nichts():
    repository = InMemoryBenutzerRepository()
    service = RegistrierungsService(repository)

    with pytest.raises(ValueError):
        service.registrieren("anna@example.com", "hash", "ADMIN")

    assert repository.finde_nach_email("anna@example.com") is None


def test_unbekannte_email_wird_nicht_gefunden():
    assert InMemoryBenutzerRepository().finde_nach_email("niemand@example.com") is None
