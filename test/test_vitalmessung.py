import pytest
from datetime import datetime
from uuid import uuid4

from meditrack.vitaldatenueberwachung.domain.model import (
    Messwert,
    Vitaltyp,
    Vitalmessung,
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


def test_vitalmessung_ohne_messung_id():
    with pytest.raises(ValueError):
        Vitalmessung(
            messung_id=None,
            patient_id=uuid4(),
            zeitpunkt=datetime.now(),
            messwert=Messwert(80, "bpm"),
            vitaltyp=Vitaltyp("Puls")
        )