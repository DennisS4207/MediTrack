from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from meditrack.alarmmanagement.application.alarm_service import AlarmService
from meditrack.alarmmanagement.domain.model import Schweregrad, Warnmeldung
from meditrack.alarmmanagement.infrastructure.in_memory_repositories import (
    InMemoryWarnmeldungRepository,
)


def _warnmeldung(**ueberschreibungen):
    parameter = {
        "warnmeldung_id": uuid4(),
        "patient_id": uuid4(),
        "aktueller_wert": 120,
        "schwellwert": 100,
        "schweregrad": Schweregrad.HOCH,
        "zeitpunkt": datetime.now(),
    }
    parameter.update(ueberschreibungen)
    return Warnmeldung(**parameter)


# Happy-Path-Tests

def test_gueltige_warnmeldung():
    patient_id = uuid4()

    warnmeldung = _warnmeldung(patient_id=patient_id)

    assert warnmeldung.patient_id == patient_id
    assert warnmeldung.aktueller_wert == 120
    assert warnmeldung.schwellwert == 100
    assert warnmeldung.schweregrad == "HOCH"
    assert warnmeldung.bestaetigt is False


def test_warnmeldung_mit_dezimalwerten():
    warnmeldung = _warnmeldung(aktueller_wert=38.7, schwellwert=38.0)

    assert warnmeldung.aktueller_wert == 38.7


def test_warnmeldung_bestaetigen_liefert_neue_warnmeldung():
    offen = _warnmeldung()

    bestaetigt = offen.als_bestaetigt()

    assert bestaetigt.bestaetigt is True
    assert offen.bestaetigt is False  # Original bleibt unverändert
    assert bestaetigt.warnmeldung_id == offen.warnmeldung_id


# Negative Tests

@pytest.mark.parametrize("feld", ["warnmeldung_id", "patient_id"])
@pytest.mark.parametrize("wert", [None, "kein-uuid"])
def test_ungueltige_ids(feld, wert):
    with pytest.raises(ValueError):
        _warnmeldung(**{feld: wert})


@pytest.mark.parametrize("wert", [None, "120", True, float("nan"), float("inf"), 10**400])
@pytest.mark.parametrize("feld", ["aktueller_wert", "schwellwert"])
def test_ungueltige_zahlenwerte(feld, wert):
    with pytest.raises(ValueError):
        _warnmeldung(**{feld: wert})


@pytest.mark.parametrize("schweregrad", [None, "", "extrem", "hoch", 3])
def test_ungueltiger_schweregrad(schweregrad):
    with pytest.raises(ValueError):
        _warnmeldung(schweregrad=schweregrad)


@pytest.mark.parametrize("zeitpunkt", [None, "2026-01-01"])
def test_ungueltiger_zeitpunkt(zeitpunkt):
    with pytest.raises(ValueError):
        _warnmeldung(zeitpunkt=zeitpunkt)


# Edge-Cases

def test_schweregrad_als_text_wird_in_enum_umgewandelt():
    assert _warnmeldung(schweregrad="NIEDRIG").schweregrad is Schweregrad.NIEDRIG


def test_wert_unter_schwellwert_ist_erlaubt():
    # Eine Warnung kann auch durch eine Unterschreitung entstehen
    warnmeldung = _warnmeldung(aktueller_wert=40, schwellwert=60)

    assert warnmeldung.aktueller_wert < warnmeldung.schwellwert


def test_negative_werte_sind_erlaubt():
    assert _warnmeldung(aktueller_wert=-5, schwellwert=-2).aktueller_wert == -5


def test_zeitpunkt_in_der_zukunft_wird_abgelehnt():
    with pytest.raises(ValueError):
        _warnmeldung(zeitpunkt=datetime.now() + timedelta(days=1))


def test_zeitpunkt_mit_zeitzone_wird_akzeptiert():
    warnmeldung = _warnmeldung(zeitpunkt=datetime.now(timezone.utc))

    assert warnmeldung.zeitpunkt.tzinfo is not None


def test_warnmeldung_ist_unveraenderlich():
    warnmeldung = _warnmeldung()

    with pytest.raises(AttributeError):
        warnmeldung.bestaetigt = True


def test_bestaetigen_ist_idempotent():
    warnmeldung = _warnmeldung().als_bestaetigt()

    assert warnmeldung.als_bestaetigt() == warnmeldung


# Application Service + Repository

def test_warnmeldung_erzeugen_speichert_sie():
    repository = InMemoryWarnmeldungRepository()
    service = AlarmService(repository)
    patient_id = uuid4()

    warnmeldung = service.warnmeldung_erzeugen(
        patient_id=patient_id,
        aktueller_wert=130,
        schwellwert=100,
        schweregrad="KRITISCH",
    )

    assert warnmeldung.patient_id == patient_id
    assert warnmeldung.schweregrad is Schweregrad.KRITISCH
    assert repository.finde_nach_id(warnmeldung.warnmeldung_id) == warnmeldung


def test_ungueltige_warnmeldung_wird_nicht_gespeichert():
    repository = InMemoryWarnmeldungRepository()
    service = AlarmService(repository)

    with pytest.raises(ValueError):
        service.warnmeldung_erzeugen(uuid4(), float("nan"), 100, "HOCH")

    assert repository.warnmeldungen == {}


def test_warnmeldung_abrufen():
    service = AlarmService(InMemoryWarnmeldungRepository())
    warnmeldung = service.warnmeldung_erzeugen(uuid4(), 130, 100, "HOCH")

    assert service.warnmeldung_abrufen(warnmeldung.warnmeldung_id) == warnmeldung


def test_unbekannte_warnmeldung_abrufen():
    service = AlarmService(InMemoryWarnmeldungRepository())

    with pytest.raises(ValueError):
        service.warnmeldung_abrufen(uuid4())


def test_warnmeldung_bestaetigen_im_service():
    repository = InMemoryWarnmeldungRepository()
    service = AlarmService(repository)
    warnmeldung = service.warnmeldung_erzeugen(uuid4(), 130, 100, "HOCH")

    bestaetigt = service.warnmeldung_bestaetigen(warnmeldung.warnmeldung_id)

    assert bestaetigt.bestaetigt is True
    assert repository.finde_nach_id(warnmeldung.warnmeldung_id).bestaetigt is True


def test_unbekannte_warnmeldung_bestaetigen():
    service = AlarmService(InMemoryWarnmeldungRepository())

    with pytest.raises(ValueError):
        service.warnmeldung_bestaetigen(uuid4())


def test_offene_warnmeldungen_nur_fuer_den_patienten_und_ohne_bestaetigte():
    service = AlarmService(InMemoryWarnmeldungRepository())
    patient_a, patient_b = uuid4(), uuid4()

    offen = service.warnmeldung_erzeugen(patient_a, 130, 100, "HOCH")
    erledigt = service.warnmeldung_erzeugen(patient_a, 140, 100, "KRITISCH")
    service.warnmeldung_erzeugen(patient_b, 150, 100, "HOCH")
    service.warnmeldung_bestaetigen(erledigt.warnmeldung_id)

    assert service.offene_warnmeldungen(patient_a) == [offen]


def test_keine_offenen_warnmeldungen_liefert_leere_liste():
    assert AlarmService(InMemoryWarnmeldungRepository()).offene_warnmeldungen(uuid4()) == []


def test_offene_warnmeldungen_sind_nach_zeitpunkt_sortiert():
    repository = InMemoryWarnmeldungRepository()
    patient_id = uuid4()
    jetzt = datetime.now()
    spaeter = _warnmeldung(patient_id=patient_id, zeitpunkt=jetzt - timedelta(minutes=1))
    frueher = _warnmeldung(patient_id=patient_id, zeitpunkt=jetzt - timedelta(hours=1))
    repository.speichern(spaeter)
    repository.speichern(frueher)

    assert repository.finde_offene_nach_patient(patient_id) == [frueher, spaeter]
