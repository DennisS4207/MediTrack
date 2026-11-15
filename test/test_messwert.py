import pytest

from meditrack.vitaldatenueberwachung.domain.model import Messwert

# Happy-Path-Tests


def test_gueltiger_messwert():
    messwert = Messwert(80, "bpm")
    assert messwert.wert == 80
    assert messwert.einheit == "bpm"


def test_dezimalwert():
    messwert = Messwert(36.5, "°C")
    assert messwert.wert == 36.5


# Edge-Cases

def test_messwert_null():
    messwert = Messwert(0, "bpm")
    assert messwert.wert == 0


def test_negative_messwerte():
    messwert = Messwert(-5, "°C")
    assert messwert.wert == -5


# Negative Tests

def test_leere_einheit():
    with pytest.raises(ValueError):
        Messwert(80, "")


def test_einheit_nur_leerzeichen():
    with pytest.raises(ValueError):
        Messwert(80, "   ")


def test_nan_wert():
    with pytest.raises(ValueError):
        Messwert(float("nan"), "bpm")


def test_unendlicher_wert():
    with pytest.raises(ValueError):
        Messwert(float("inf"), "bpm")


@pytest.mark.parametrize("wert", [-float("inf"), None, "80", True, 10**400])
def test_unzulaessige_werte(wert):
    # Auch Nicht-Zahlen und zu große Ganzzahlen müssen als ValueError abgelehnt werden
    with pytest.raises(ValueError):
        Messwert(wert, "bpm")


@pytest.mark.parametrize("einheit", [None, 5])
def test_einheit_muss_text_sein(einheit):
    with pytest.raises(ValueError):
        Messwert(80, einheit)


def test_gleiche_messwerte_sind_gleich():
    assert Messwert(80, "bpm") == Messwert(80, "bpm")
    assert Messwert(80, "bpm") != Messwert(81, "bpm")
    assert Messwert(80, "bpm") != Messwert(80, "mmHg")


# Unveränderlichkeit des Value Objects

def test_messwert_ist_unveraenderlich():
    messwert = Messwert(80, "bpm")

    with pytest.raises(AttributeError):
        messwert.wert = 90
