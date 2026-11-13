import pytest
from uuid import uuid4

from meditrack.benutzerverwaltung.domain.model import Benutzerkonto, Benutzerrolle


# Happy-Path-Tests

def test_gueltiges_benutzerkonto():
    konto = Benutzerkonto(
        benutzer_id=uuid4(),
        email="max@example.com",
        passwort_hash="gesicherter_hash",
        rolle=Benutzerrolle.PATIENT    )

    assert konto.email == "max@example.com"
    assert konto.rolle == "PATIENT"


def test_mitarbeiterkonto():
    konto = Benutzerkonto(
        benutzer_id=uuid4(),
        email="arzt@example.com",
        passwort_hash="gesicherter_hash",
        rolle=Benutzerrolle.MITARBEITER    )

    assert konto.rolle == "MITARBEITER"


# Negative Tests

def test_leere_email():
    with pytest.raises(ValueError):
        Benutzerkonto(
            uuid4(), "", "hash", "PATIENT"
        )


def test_ungueltige_email():
    with pytest.raises(ValueError):
        Benutzerkonto(
            uuid4(), "ungueltige-email", "hash", "PATIENT"
        )


def test_leerer_passwort_hash():
    with pytest.raises(ValueError):
        Benutzerkonto(
            uuid4(), "max@example.com", "", "PATIENT"
        )


def test_ungueltige_rolle():
    with pytest.raises(ValueError):
        Benutzerkonto(
            uuid4(), "max@example.com", "hash", "ADMIN"
        )


# Edge-Cases

def test_email_mit_pluszeichen():
    konto = Benutzerkonto(
        uuid4(), "max+test@example.com", "hash", "PATIENT"
    )

    assert konto.email == "max+test@example.com"


def test_fehlende_benutzer_id():
    with pytest.raises(ValueError):
        Benutzerkonto(
            None, "max@example.com", "hash", "PATIENT"
        )


from meditrack.benutzerverwaltung.application.registrierungs_service import (
    RegistrierungsService
)
from meditrack.benutzerverwaltung.infrastructure.in_memory_repositories import (
    InMemoryBenutzerRepository
)


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


def test_registrierung_mit_ungueltiger_email():
    repository = InMemoryBenutzerRepository()
    service = RegistrierungsService(repository)

    with pytest.raises(ValueError):
        service.registrieren(
            email="ungueltig",
            passwort_hash="gesicherter_hash",
            rolle="PATIENT"
        )