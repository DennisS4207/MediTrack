"""Tests für die Backend-Anbindung des Frontends (frontend/backend.py)."""
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest

WURZEL = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(WURZEL), str(WURZEL / "frontend")]

from backend import MeditrackBackend, demo_daten_laden, schweregrad_fuer, VITALTYPEN  # noqa: E402
from meditrack.alarmmanagement.domain.model import Schweregrad  # noqa: E402


def _backend_mit_patient():
    b = MeditrackBackend()
    return b, b.patient_anlegen("Erika", "Muster", date(1980, 5, 1))


def test_wert_im_normalbereich_erzeugt_keine_warnmeldung():
    b, p = _backend_mit_patient()
    messung, warnung = b.messung_erfassen(p.patient_id, "Puls", 72)
    assert warnung is None
    assert b.messungen(p.patient_id) == [messung]
    assert b.offene_warnmeldungen(p.patient_id) == []


def test_kritischer_wert_erzeugt_warnmeldung_mit_grenze():
    b, p = _backend_mit_patient()
    _, warnung = b.messung_erfassen(p.patient_id, "Sauerstoffsättigung", 86)
    assert warnung is not None
    assert warnung.schwellwert == 92
    assert warnung.schweregrad == Schweregrad.KRITISCH
    assert b.warn_vitaltyp[warnung.warnmeldung_id] == "Sauerstoffsättigung"


def test_bestaetigte_warnmeldung_ist_nicht_mehr_offen():
    b, p = _backend_mit_patient()
    _, warnung = b.messung_erfassen(p.patient_id, "Puls", 150)
    b.warnung_bestaetigen(warnung.warnmeldung_id)
    assert b.offene_warnmeldungen() == []
    assert len(b.alle_warnmeldungen()) == 1


def test_offene_warnmeldungen_nach_schweregrad_sortiert():
    b, p = _backend_mit_patient()
    b.messung_erfassen(p.patient_id, "Puls", 122)  # knapp über der Grenze
    b.messung_erfassen(p.patient_id, "Sauerstoffsättigung", 80)  # weit darunter
    assert [w.schweregrad for w in b.offene_warnmeldungen()][0] == Schweregrad.KRITISCH


def test_messung_fuer_unbekannten_patienten_wird_abgelehnt():
    from uuid import uuid4
    with pytest.raises(ValueError):
        MeditrackBackend().messung_erfassen(uuid4(), "Puls", 70)


def test_ungueltiger_messwert_wird_abgelehnt():
    b, p = _backend_mit_patient()
    with pytest.raises(ValueError):
        b.messung_erfassen(p.patient_id, "Puls", float("nan"))


def test_behandlung_wird_dokumentiert_und_im_verlauf_angezeigt():
    b, p = _backend_mit_patient()
    konto = b.registrieren("arzt@klinik.de", "geheim-123", "MITARBEITER")
    b.behandlung_dokumentieren(p.patient_id, konto.benutzer_id, "Infusion gestartet", "500 ml NaCl")
    assert [v.massnahme for v in b.verlauf(p.patient_id)] == ["Infusion gestartet"]


def test_leere_massnahme_wird_abgelehnt():
    b, p = _backend_mit_patient()
    konto = b.registrieren("arzt@klinik.de", "geheim-123", "MITARBEITER")
    with pytest.raises(ValueError):
        b.behandlung_dokumentieren(p.patient_id, konto.benutzer_id, "  ")


def test_anmeldung_mit_richtigem_und_falschem_passwort():
    b = MeditrackBackend()
    b.registrieren("pflege@klinik.de", "geheim-123", "MITARBEITER")
    assert b.anmelden("PFLEGE@klinik.de", "geheim-123").rolle.value == "MITARBEITER"
    with pytest.raises(ValueError):
        b.anmelden("pflege@klinik.de", "falsch")
    with pytest.raises(ValueError):
        b.anmelden("unbekannt@klinik.de", "geheim-123")


def test_registrierung_prueft_passwortlaenge_und_doppelte_email():
    b = MeditrackBackend()
    with pytest.raises(ValueError):
        b.registrieren("a@b.de", "kurz", "PATIENT")
    b.registrieren("a@b.de", "langes-passwort", "PATIENT")
    with pytest.raises(ValueError):
        b.registrieren("a@b.de", "langes-passwort", "PATIENT")


def test_schweregrad_waechst_mit_dem_abstand():
    regel = VITALTYPEN["Puls"][1]  # 50 bis 120
    assert schweregrad_fuer(regel, 121) == Schweregrad.NIEDRIG
    assert schweregrad_fuer(regel, 125) == Schweregrad.MITTEL
    assert schweregrad_fuer(regel, 135) == Schweregrad.HOCH
    assert schweregrad_fuer(regel, 160) == Schweregrad.KRITISCH


def test_demo_daten_enthalten_patienten_messungen_und_warnmeldungen():
    b = MeditrackBackend()
    demo_daten_laden(b)
    assert len(b.alle_patienten()) == 3
    assert all(b.messungen(p.patient_id) for p in b.alle_patienten())
    assert len(b.offene_warnmeldungen()) >= 1


def test_patient_registriert_sich_mit_hinterlegter_email_und_wird_verknuepft():
    b = MeditrackBackend()
    patient = b.patient_anlegen_mit_email("Erika", "Muster", date(1980, 5, 1), "Erika@Mail.de")
    assert not b.hat_konto(patient.patient_id)
    konto = b.patient_registrieren("erika@mail.de", "langes-passwort")
    assert konto.rolle.value == "PATIENT"
    assert b.patient_id_fuer(konto) == patient.patient_id
    assert b.hat_konto(patient.patient_id)
    assert b.patient_id_fuer(b.anmelden("ERIKA@mail.de", "langes-passwort")) == patient.patient_id


def test_registrierung_ohne_patientenakte_wird_abgelehnt():
    b = MeditrackBackend()
    with pytest.raises(ValueError):
        b.patient_registrieren("fremd@mail.de", "langes-passwort")
    assert b.benutzer_repo.finde_nach_email("fremd@mail.de") is None


def test_selbstregistrierung_erzeugt_nie_ein_mitarbeiterkonto():
    b = MeditrackBackend()
    b.patient_anlegen_mit_email("Erika", "Muster", date(1980, 5, 1), "erika@mail.de")
    assert b.patient_registrieren("erika@mail.de", "langes-passwort").rolle.value == "PATIENT"


def test_patient_kann_sich_nicht_zweimal_registrieren():
    b = MeditrackBackend()
    b.patient_anlegen_mit_email("Erika", "Muster", date(1980, 5, 1), "erika@mail.de")
    b.patient_registrieren("erika@mail.de", "langes-passwort")
    with pytest.raises(ValueError):
        b.patient_registrieren("erika@mail.de", "anderes-passwort")


def test_zu_kurzes_passwort_bei_registrierung_wird_abgelehnt():
    b = MeditrackBackend()
    p = b.patient_anlegen_mit_email("Erika", "Muster", date(1980, 5, 1), "erika@mail.de")
    with pytest.raises(ValueError):
        b.patient_registrieren("erika@mail.de", "kurz")
    assert not b.hat_konto(p.patient_id)


def test_ungueltige_email_legt_keinen_patienten_an():
    b = MeditrackBackend()
    with pytest.raises(ValueError):
        b.patient_anlegen_mit_email("Erika", "Muster", date(1980, 5, 1), "keine-email")
    assert b.alle_patienten() == []


def test_doppelte_email_legt_keinen_zweiten_patienten_an():
    b = MeditrackBackend()
    b.patient_anlegen_mit_email("Erika", "Muster", date(1980, 5, 1), "erika@mail.de")
    with pytest.raises(ValueError):
        b.patient_anlegen_mit_email("Anna", "Beispiel", date(1990, 1, 1), "Erika@Mail.de")
    assert len(b.alle_patienten()) == 1


def test_ungueltiger_name_hinterlegt_keine_email():
    b = MeditrackBackend()
    with pytest.raises(ValueError):
        b.patient_anlegen_mit_email("  ", "Muster", date(1980, 5, 1), "erika@mail.de")
    assert b.patient_email == {}


def test_konto_ohne_verknuepfung_hat_keine_patientenakte():
    b = MeditrackBackend()
    konto = b.registrieren("lose@mail.de", "langes-passwort", "PATIENT")
    assert b.patient_id_fuer(konto) is None


def test_demo_patientenkonto_ist_mit_akte_verknuepft():
    b = MeditrackBackend()
    demo_daten_laden(b)
    pid = b.patient_id_fuer(b.anmelden("patient@meditrack.test", "demo-passwort"))
    assert pid is not None and b.messungen(pid)


def test_demo_patient_karl_kann_sich_registrieren():
    b = MeditrackBackend()
    demo_daten_laden(b)
    konto = b.patient_registrieren("karl@meditrack.test", "langes-passwort")
    assert b.patient_id_fuer(konto) is not None
