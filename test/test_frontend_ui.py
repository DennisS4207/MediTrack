"""UI-Tests der Streamlit-App mit streamlit.testing.v1.AppTest (headless, ohne Browser)."""
import sys
from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

APP = str(Path(__file__).resolve().parent.parent / "frontend" / "app.py")
sys.path[:0] = [str(Path(APP).parent.parent), str(Path(APP).parent)]


def _angemeldet():
    at = AppTest.from_file(APP, default_timeout=30)
    at.run()
    at.text_input(key="login_email").input("pflege@meditrack.test")
    at.text_input(key="login_pw").input("demo-passwort")
    at.button[0].click().run()
    return at


def test_login_seite_wird_angezeigt():
    at = AppTest.from_file(APP, default_timeout=30).run()
    assert not at.exception
    assert "MediTrack" in at.title[0].value


def test_falsches_passwort_zeigt_fehler():
    at = AppTest.from_file(APP, default_timeout=30).run()
    at.text_input(key="login_email").input("pflege@meditrack.test")
    at.text_input(key="login_pw").input("falsch")
    at.button[0].click().run()
    assert any("falsch" in e.value for e in at.error)


def test_anmeldung_zeigt_stationsuebersicht_mit_demodaten():
    at = _angemeldet()
    assert not at.exception
    assert at.title[0].value == "Stationsübersicht"
    assert at.metric[0].label == "Patienten" and int(at.metric[0].value) >= 3


def test_navigation_zu_allen_seiten_ohne_fehler():
    at = _angemeldet()
    for seite in ["Patientenakte", "Patient anlegen", "Warnmeldungen"]:
        at.radio(key="nav").set_value(seite).run()
        assert not at.exception, seite


def test_patient_anlegen_ueber_formular():
    at = _angemeldet()
    at.radio(key="nav").set_value("Patient anlegen").run()
    at.text_input(key="pat_vorname").input("Max")
    at.text_input(key="pat_nachname").input("Beispiel")
    at.text_input(key="pat_email").input("max@beispiel.de")
    at.button[0].click().run()
    assert not at.exception
    assert any("Max Beispiel" in s.value for s in at.success)


def test_patient_anlegen_ohne_email_zeigt_fehler():
    at = _angemeldet()
    at.radio(key="nav").set_value("Patient anlegen").run()
    at.text_input(key="pat_vorname").input("Eva")
    at.text_input(key="pat_nachname").input("Ohne")
    at.button[0].click().run()
    assert any("E-Mail" in e.value for e in at.error)


def test_patientenkonto_sieht_nur_die_eigene_akte_ohne_erfassen():
    at = AppTest.from_file(APP, default_timeout=30).run()
    at.text_input(key="login_email").input("patient@meditrack.test")
    at.text_input(key="login_pw").input("demo-passwort")
    at.button[0].click().run()
    assert not at.exception
    assert at.title[0].value == "Meine Akte"
    assert all(r.key != "nav" for r in at.radio)  # keine Personal-Navigation
    assert [t.label for t in at.tabs] == ["Vitalwerte", "Behandlungsverlauf"]


def test_registrierung_ohne_patientenakte_zeigt_fehler_und_legt_kein_konto_an():
    at = AppTest.from_file(APP, default_timeout=30).run()
    at.text_input(key="reg_email").input("fremd@mail.de")
    at.text_input(key="reg_pw").input("langes-passwort")
    at.text_input(key="reg_pw2").input("langes-passwort")
    at.button[1].click().run()
    assert any("Patientenakte" in e.value for e in at.error)
    assert all(s.key != "reg_rolle" for s in at.selectbox)  # keine Rollenauswahl mehr
    at.text_input(key="login_email").input("fremd@mail.de")
    at.text_input(key="login_pw").input("langes-passwort")
    at.button[0].click().run()
    assert any("falsch" in e.value for e in at.error)


def test_registrierung_mit_hinterlegter_email_fuehrt_zur_eigenen_akte():
    at = AppTest.from_file(APP, default_timeout=30).run()
    at.text_input(key="reg_email").input("karl@meditrack.test")
    at.text_input(key="reg_pw").input("langes-passwort")
    at.text_input(key="reg_pw2").input("langes-passwort")
    at.button[1].click().run()
    assert any("Registrierung abgeschlossen" in x.value for x in at.success)
    at.text_input(key="login_email").input("karl@meditrack.test")
    at.text_input(key="login_pw").input("langes-passwort")
    at.button[0].click().run()
    assert at.title[0].value == "Meine Akte"
    assert all(r.key != "nav" for r in at.radio)  # kein Zugriff auf die Personal-Navigation
