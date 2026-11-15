from datetime import date, datetime, timedelta
from uuid import uuid4

import pytest

from meditrack.patientenverwaltung.application.patienten_service import PatientenService
from meditrack.patientenverwaltung.domain.model import Patient
from meditrack.patientenverwaltung.infrastructure.in_memory_repositories import (
    InMemoryPatientenRepository,
)

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


def test_geburtsdatum_heute_ist_erlaubt():
    patient = Patient(uuid4(), "Baby", "Müller", date.today())

    assert patient.geburtsdatum == date.today()


def test_geburtsdatum_als_datetime_wird_abgelehnt():
    # datetime ist eine Unterklasse von date, darf aber nicht zu einem TypeError führen
    with pytest.raises(ValueError):
        Patient(uuid4(), "Anna", "Müller", datetime.now())


def test_geburtsdatum_als_text_wird_abgelehnt():
    with pytest.raises(ValueError):
        Patient(uuid4(), "Anna", "Müller", "1995-05-15")


def test_vorname_nur_leerzeichen():
    with pytest.raises(ValueError):
        Patient(uuid4(), "   ", "Müller", date(1995, 5, 15))


def test_nachname_nur_leerzeichen():
    with pytest.raises(ValueError):
        Patient(uuid4(), "Anna", "   ", date(1995, 5, 15))


@pytest.mark.parametrize("name", [None, 42, ["Anna"]])
def test_namen_muessen_texte_sein(name):
    with pytest.raises(ValueError):
        Patient(uuid4(), name, "Müller", date(1995, 5, 15))

    with pytest.raises(ValueError):
        Patient(uuid4(), "Anna", name, date(1995, 5, 15))


def test_patient_id_als_text_wird_abgelehnt():
    with pytest.raises(ValueError):
        Patient(str(uuid4()), "Anna", "Müller", date(1995, 5, 15))


# Application Service + Repository

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


def test_fehlgeschlagenes_anlegen_speichert_nichts():
    repository = InMemoryPatientenRepository()
    service = PatientenService(repository)

    with pytest.raises(ValueError):
        service.patient_anlegen("", "Müller", date(1995, 5, 15))

    assert repository.patienten == {}


def test_gleichnamige_patienten_erhalten_verschiedene_ids():
    service = PatientenService(InMemoryPatientenRepository())

    erster = service.patient_anlegen("Anna", "Müller", date(1995, 5, 15))
    zweiter = service.patient_anlegen("Anna", "Müller", date(1995, 5, 15))

    assert erster.patient_id != zweiter.patient_id
    assert service.patient_abrufen(erster.patient_id) is erster
    assert service.patient_abrufen(zweiter.patient_id) is zweiter


def test_unbekannte_id_liefert_im_repository_none():
    assert InMemoryPatientenRepository().finde_nach_id(uuid4()) is None
