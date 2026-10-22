# Testet die Patientenverwaltung.
# Prüft beispielsweise, ob Patienten
# korrekt angelegt werden können.



import pytest
import patient


@pytest.fixture(autouse=True)
def patienten_zuruecksetzen():
    patient.patienten.clear()
    yield
    patient.patienten.clear()


# Test 1: Patient hinzufügen
def test_patient_hinzufuegen():
    patient.patient_hinzufuegen(1, "Max", 25)

    assert patient.patient_suchen(1) == {
        "name": "Max",
        "alter": 25
    }


# Test 2: Patient suchen
def test_patient_suchen():
    patient.patient_hinzufuegen(2, "Anna", 30)

    ergebnis = patient.patient_suchen(2)

    assert ergebnis["name"] == "Anna"
    assert ergebnis["alter"] == 30


# Test 3: Patient löschen
def test_patient_loeschen():
    patient.patient_hinzufuegen(3, "Tom", 40)

    ergebnis = patient.patient_loeschen(3)

    assert ergebnis is True
    assert patient.patient_suchen(3) is None
