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


@pytest.mark.parametrize("minimum, maximum", [(None, 100), (60, "100"), (True, 100), (60, 10**400)])
def test_grenzwerte_muessen_zahlen_sein(minimum, maximum):
    with pytest.raises(ValueError):
        Grenzwertregel(minimum, maximum)


@pytest.mark.parametrize("wert", [float("nan"), float("inf"), -float("inf"), None, "80", True])
def test_ungueltiger_vitalwert_bei_pruefung(wert):
    with pytest.raises(ValueError):
        Grenzwertregel(60, 100).ist_kritisch(wert)


@pytest.mark.parametrize("wert, erwartet", [(59.999, True), (100.001, True), (60.0, False), (100.0, False)])
def test_grenzen_mit_nachkommastellen(wert, erwartet):
    assert Grenzwertregel(60, 100).ist_kritisch(wert) is erwartet


def test_negative_grenzwerte():
    regel = Grenzwertregel(-10, -5)

    assert regel.ist_kritisch(-7) is False
    assert regel.ist_kritisch(0) is True


def test_identische_grenzwerte_abweichender_wert_ist_kritisch():
    assert Grenzwertregel(80, 80).ist_kritisch(81) is True
    assert Grenzwertregel(80, 80).ist_kritisch(79) is True


def test_grenzwertregel_ist_unveraenderlich():
    regel = Grenzwertregel(60, 100)

    with pytest.raises(AttributeError):
        regel.maximum = 200
