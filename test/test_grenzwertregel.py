import pytest

from meditrack.vitaldatenueberwachung.domain.model import Grenzwertregel


# Happy-Path-Tests

def test_normaler_vitalwert():
    regel = Grenzwertregel(60, 100)
    assert regel.ist_kritisch(80) is False


def test_zu_hoher_vitalwert():
    regel = Grenzwertregel(60, 100)
    assert regel.ist_kritisch(120) is True


def test_zu_niedriger_vitalwert():
    regel = Grenzwertregel(60, 100)
    assert regel.ist_kritisch(45) is True


# Edge-Cases

def test_untere_grenze():
    regel = Grenzwertregel(60, 100)
    assert regel.ist_kritisch(60) is False


def test_obere_grenze():
    regel = Grenzwertregel(60, 100)
    assert regel.ist_kritisch(100) is False


def test_identische_grenzwerte():
    regel = Grenzwertregel(80, 80)
    assert regel.ist_kritisch(80) is False


# Negative Tests

def test_ungueltige_grenzwerte():
    with pytest.raises(ValueError):
        Grenzwertregel(100, 60)


def test_nan_grenzwert():
    with pytest.raises(ValueError):
        Grenzwertregel(float("nan"), 100)


def test_unendlicher_grenzwert():
    with pytest.raises(ValueError):
        Grenzwertregel(60, float("inf"))