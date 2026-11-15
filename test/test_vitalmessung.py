from datetime import datetime
from uuid import uuid4

import pytest

from meditrack.vitaldatenueberwachung.domain.model import (
    Messwert,
    Vitalmessung,
    Vitaltyp,
)

# Happy-Path-Tests


def test_gueltige_vitalmessung():
    patient_id = uuid4()
    messung_id = uuid4()

    messung = Vitalmessung(
        messung_id=messung_id,
        patient_id=patient_id,
        zeitpunkt=datetime.now(),
        messwert=Messwert(80, "bpm"),
        vitaltyp=Vitaltyp("Puls")
    )

    assert messung.patient_id == patient_id
    assert messung.messwert.wert == 80
    assert messung.vitaltyp.bezeichnung == "Puls"


def test_temperaturmessung():
    messung = Vitalmessung(
        messung_id=uuid4(),
        patient_id=uuid4(),
        zeitpunkt=datetime.now(),
        messwert=Messwert(36.5, "°C"),
        vitaltyp=Vitaltyp("Temperatur")
    )

    assert messung.messwert.wert == 36.5


# Negative Tests

def test_vitalmessung_ohne_patient():
    with pytest.raises(ValueError):
        Vitalmessung(
            messung_id=uuid4(),
            patient_id=None,
            zeitpunkt=datetime.now(),
            messwert=Messwert(80, "bpm"),
            vitaltyp=Vitaltyp("Puls")
        )


def test_vitalmessung_ohne_messwert():
    with pytest.raises(ValueError):
        Vitalmessung(
            messung_id=uuid4(),
            patient_id=uuid4(),
            zeitpunkt=datetime.now(),
            messwert=None,
            vitaltyp=Vitaltyp("Puls")
        )


def test_vitalmessung_ohne_vitaltyp():
    with pytest.raises(ValueError):
        Vitalmessung(
            messung_id=uuid4(),
            patient_id=uuid4(),
            zeitpunkt=datetime.now(),
            messwert=Messwert(80, "bpm"),
            vitaltyp=None
        )


def test_vitalmessung_ohne_zeitpunkt():
    with pytest.raises(ValueError):
        Vitalmessung(
            messung_id=uuid4(),
            patient_id=uuid4(),
            zeitpunkt=None,
            messwert=Messwert(80, "bpm"),
            vitaltyp=Vitaltyp("Puls")
        )


# Edge-Cases

def test_vitaltyp_ohne_bezeichnung():
    with pytest.raises(ValueError):
        Vitaltyp("")


def test_vitaltyp_nur_leerzeichen():
    with pytest.raises(ValueError):
        Vitaltyp("   ")


@pytest.mark.parametrize("bezeichnung", [None, 42])
def test_vitaltyp_muss_text_sein(bezeichnung):
    with pytest.raises(ValueError):
        Vitaltyp(bezeichnung)


@pytest.mark.parametrize("feld", ["messung_id", "patient_id"])
def test_ids_als_text_werden_abgelehnt(feld):
    parameter = {
        "messung_id": uuid4(),
        "patient_id": uuid4(),
        "zeitpunkt": datetime.now(),
        "messwert": Messwert(80, "bpm"),
        "vitaltyp": Vitaltyp("Puls"),
    }
    parameter[feld] = str(parameter[feld])

    with pytest.raises(ValueError):
        Vitalmessung(**parameter)


def test_zeitpunkt_als_text_wird_abgelehnt():
    with pytest.raises(ValueError):
        Vitalmessung(uuid4(), uuid4(), "2026-01-01", Messwert(80, "bpm"), Vitaltyp("Puls"))


def test_messwert_als_zahl_wird_abgelehnt():
    with pytest.raises(ValueError):
        Vitalmessung(uuid4(), uuid4(), datetime.now(), 80, Vitaltyp("Puls"))


def test_vitalmessung_ist_unveraenderlich():
    messung = Vitalmessung(uuid4(), uuid4(), datetime.now(), Messwert(80, "bpm"), Vitaltyp("Puls"))

    with pytest.raises(AttributeError):
        messung.messwert = Messwert(90, "bpm")


def test_vitalmessung_ohne_messung_id():
    with pytest.raises(ValueError):
        Vitalmessung(
            messung_id=None,
            patient_id=uuid4(),
            zeitpunkt=datetime.now(),
            messwert=Messwert(80, "bpm"),
            vitaltyp=Vitaltyp("Puls")
        )
