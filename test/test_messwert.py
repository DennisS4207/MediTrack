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


# Unveränderlichkeit des Value Objects

def test_messwert_ist_unveraenderlich():
    messwert = Messwert(80, "bpm")

    with pytest.raises(AttributeError):
        messwert.wert = 90