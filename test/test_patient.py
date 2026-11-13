import pytest
from uuid import uuid4
from datetime import date, timedelta

from meditrack.patientenverwaltung.domain.model import Patient


# Happy-Path-Tests

def test_gueltiger_patient():
    patient_id = uuid4()

    patient = Patient(
        patient_id=patient_id,
        vorname="Anna",
        nachname="Müller",
        geburtsdatum=date(1995, 5, 15)
    )

    assert patient.patient_id == patient_id
    assert patient.vorname == "Anna"
    assert patient.nachname == "Müller"
    assert patient.geburtsdatum == date(1995, 5, 15)


def test_patient_mit_bindestrich_im_namen():
    patient = Patient(
        patient_id=uuid4(),
        vorname="Anna-Maria",
        nachname="Müller-Schmidt",
        geburtsdatum=date(1990, 3, 10)
    )

    assert patient.vorname == "Anna-Maria"


# Negative Tests

def test_leerer_vorname():
    with pytest.raises(ValueError):
        Patient(uuid4(), "", "Müller", date(1995, 5, 15))


def test_leerer_nachname():
    with pytest.raises(ValueError):
        Patient(uuid4(), "Anna", "", date(1995, 5, 15))


def test_fehlende_patienten_id():
    with pytest.raises(ValueError):
        Patient(None, "Anna", "Müller", date(1995, 5, 15))


def test_fehlendes_geburtsdatum():
    with pytest.raises(ValueError):
        Patient(uuid4(), "Anna", "Müller", None)


# Edge-Cases

def test_geburtsdatum_in_der_zukunft():
    morgen = date.today() + timedelta(days=1)

    with pytest.raises(ValueError):
        Patient(uuid4(), "Anna", "Müller", morgen)


def test_vorname_nur_leerzeichen():
    with pytest.raises(ValueError):
        Patient(uuid4(), "   ", "Müller", date(1995, 5, 15))


def test_nachname_nur_leerzeichen():
    with pytest.raises(ValueError):
        Patient(uuid4(), "Anna", "   ", date(1995, 5, 15))

from meditrack.patientenverwaltung.application.patienten_service import (
    PatientenService
)
from meditrack.patientenverwaltung.infrastructure.in_memory_repositories import (
    InMemoryPatientenRepository
)


def test_patient_anlegen():
    repository = InMemoryPatientenRepository()
    service = PatientenService(repository)

    patient = service.patient_anlegen(
        vorname="Anna",
        nachname="Müller",
        geburtsdatum=date(1995, 5, 15)
    )

    assert patient.vorname == "Anna"
    assert patient.nachname == "Müller"
    assert repository.finde_nach_id(patient.patient_id) == patient


def test_patient_abrufen():
    repository = InMemoryPatientenRepository()
    service = PatientenService(repository)

    patient = service.patient_anlegen(
        vorname="Max",
        nachname="Schmidt",
        geburtsdatum=date(1990, 3, 10)
    )

    gefundener_patient = service.patient_abrufen(patient.patient_id)

    assert gefundener_patient == patient


def test_nicht_existierenden_patienten_abrufen():
    repository = InMemoryPatientenRepository()
    service = PatientenService(repository)

    with pytest.raises(ValueError):
        service.patient_abrufen(uuid4())


def test_patient_mit_ungueltigem_geburtsdatum_anlegen():
    repository = InMemoryPatientenRepository()
    service = PatientenService(repository)

    with pytest.raises(ValueError):
        service.patient_anlegen(
            vorname="Anna",
            nachname="Müller",
            geburtsdatum=date.today() + timedelta(days=1)
        )