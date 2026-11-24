"""MediTrack-Frontend (Streamlit).

Start im Projektstamm (dort, wo der Ordner `meditrack/` liegt):
    streamlit run frontend/app.py
"""
import os
import smtplib
import sys
from datetime import date, datetime
from email.message import EmailMessage
from pathlib import Path

ORDNER = Path(__file__).resolve().parent
WURZEL = ORDNER.parent
sys.path[:0] = [str(WURZEL), str(ORDNER)]

import pandas as pd  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
import streamlit as st  # noqa: E402

from backend import VITALTYPEN, MeditrackBackend, demo_daten_laden  # noqa: E402

SCHWERE = {"KRITISCH": "🔴 Kritisch", "HOCH": "🔴 Hoch", "MITTEL": "🟠 Mittel", "NIEDRIG": "🟡 Niedrig"}
RANG = {"KRITISCH": 0, "HOCH": 1, "MITTEL": 2, "NIEDRIG": 3}

st.set_page_config(page_title="MediTrack", page_icon="🩺", layout="wide")
st.markdown(f"<style>{(ORDNER / 'glass.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


@st.cache_resource
def get_backend() -> MeditrackBackend:
    """Eine Backend-Instanz pro Prozess. Die Daten liegen im Arbeitsspeicher (In-Memory-Repositories)."""
    b = MeditrackBackend()
    if os.getenv("MEDITRACK_DEMO", "1") == "1":
        demo_daten_laden(b)
    return b


def send_mail(betreff: str, text: str) -> bool:
    """Optionale E-Mail bei kritischen Werten (SMTP_HOST und ALERT_MAIL_TO müssen gesetzt sein)."""
    host, to = os.getenv("SMTP_HOST"), os.getenv("ALERT_MAIL_TO")
    if not (host and to):
        return False
    try:
        msg = EmailMessage()
        msg["Subject"], msg["To"] = betreff, to
        msg["From"] = os.getenv("SMTP_FROM", os.getenv("SMTP_USER", "meditrack@localhost"))
        msg.set_content(text)
        with smtplib.SMTP(host, int(os.getenv("SMTP_PORT", "587"))) as s:
            s.starttls()
            if os.getenv("SMTP_USER"):
                s.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD", ""))
            s.send_message(msg)
        return True
    except Exception:
        return False


def flash(art: str, text: str):
    st.session_state["flash"] = (art, text)


def zeige_flash():
    f = st.session_state.pop("flash", None)
    if f:
        getattr(st, f[0])(f[1])


def name(p) -> str:
    return f"{p.vorname} {p.nachname}"


def alter(geb: date) -> int:
    heute = date.today()
    return heute.year - geb.year - ((heute.month, heute.day) < (geb.month, geb.day))


# ---------------------------------------------------------------- Anmeldung
def seite_login(b: MeditrackBackend):
    _, mitte, _ = st.columns([1, 1.3, 1])
    with mitte:
        st.title("🩺 MediTrack")
        st.caption("Patientendaten verwalten und überwachen")
        tab_a, tab_r = st.tabs(["Anmelden", "Registrieren"])
        with tab_a.form("login"):
            email = st.text_input("E-Mail", key="login_email")
            pw = st.text_input("Passwort", type="password", key="login_pw")
            if st.form_submit_button("Anmelden"):
                try:
                    st.session_state["user"] = b.anmelden(email, pw)
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
        with tab_r.form("register"):  # nur Mitarbeiterkonten
            email = st.text_input("E-Mail", key="reg_email")
            pw = st.text_input("Passwort (mindestens 8 Zeichen)", type="password", key="reg_pw")
            st.caption("Patientenkonten legt das Personal beim Anlegen des Patienten an.")
            if st.form_submit_button("Konto anlegen"):
                try:
                    b.registrieren(email, pw, "MITARBEITER")
                    st.success("Konto angelegt. Du kannst dich jetzt anmelden.")
                except ValueError as e:
                    st.error(str(e))
        if os.getenv("MEDITRACK_DEMO", "1") == "1":
            st.caption("Demo-Zugang: pflege@meditrack.test, Passwort demo-passwort")


# ---------------------------------------------------------------- Seiten
@st.fragment(run_every=30)
def seite_uebersicht(b: MeditrackBackend):
    st.title("Stationsübersicht")
    zeige_flash()
    patienten = {p.patient_id: p for p in b.alle_patienten()}
    offen = b.offene_warnmeldungen()
    c = st.columns(3)
    c[0].metric("Patienten", len(patienten))
    c[1].metric("Offene Warnmeldungen", len(offen))
    c[2].metric("Davon kritisch oder hoch", sum(w.schweregrad.value in ("KRITISCH", "HOCH") for w in offen))

    st.subheader("Offene Warnmeldungen")
    if not offen:
        st.success("Keine offenen Warnmeldungen.")
    for w in offen[:15]:
        p = patienten[w.patient_id]
        typ = b.warn_vitaltyp.get(w.warnmeldung_id, "Messwert")
        c1, c2 = st.columns([6, 1])
        box = c1.error if w.schweregrad.value in ("KRITISCH", "HOCH") else c1.warning
        box(f"**{name(p)}**: {typ} {w.aktueller_wert:g} (Grenze {w.schwellwert:g}), {SCHWERE[w.schweregrad.value]}, "
            f"{w.zeitpunkt:%d.%m. %H:%M}")
        if c2.button("Bestätigen", key=f"ack_{w.warnmeldung_id}"):
            b.warnung_bestaetigen(w.warnmeldung_id)
            st.rerun()

    st.subheader("Patienten")
    zeilen = []
    for p in patienten.values():
        eigene = [w for w in offen if w.patient_id == p.patient_id]
        schlimmste = min((w.schweregrad.value for w in eigene), key=RANG.get, default=None)
        letzte = {m.vitaltyp.bezeichnung: m.messwert.wert for m in b.messungen(p.patient_id)}
        zeilen.append({"Dringlichkeit": RANG.get(schlimmste, 9),
                       "Status": SCHWERE.get(schlimmste, "🟢 Stabil"), "Name": name(p), "Alter": alter(p.geburtsdatum),
                       **{t: letzte.get(t) for t in VITALTYPEN}})
    if zeilen:
        df = pd.DataFrame(zeilen).sort_values("Dringlichkeit").drop(columns="Dringlichkeit")
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.info("Noch keine Patienten. Lege unter „Patient anlegen“ den ersten an.")


def vital_chart(messungen, typ):
    einheit, regel = VITALTYPEN[typ]
    daten = [m for m in messungen if m.vitaltyp.bezeichnung == typ]
    x = [m.zeitpunkt for m in daten]
    y = [m.messwert.wert for m in daten]
    fig = go.Figure()
    fig.add_hrect(y0=regel.minimum, y1=regel.maximum, fillcolor="#2E7D5B", opacity=0.14, line_width=0)
    for grenze in (regel.minimum, regel.maximum):
        fig.add_hline(y=grenze, line_dash="dot", line_color="#C8321E")
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", line=dict(color="#0E7C86", width=3, shape="spline", smoothing=0.6),
                             marker=dict(size=9, line=dict(color="white", width=1.5),
                                         color=["#D6452D" if regel.ist_kritisch(v) else "#0E7C86" for v in y])))
    fig.update_layout(height=320, showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=10, r=10, t=10, b=10), yaxis_title=f"{typ} ({einheit})",
                      font=dict(family="Manrope, sans-serif", color="#0F2E35"))
    fig.update_xaxes(gridcolor="rgba(15,46,53,0.08)")
    fig.update_yaxes(gridcolor="rgba(15,46,53,0.08)")
    st.plotly_chart(fig, use_container_width=True)


def seite_patient(b: MeditrackBackend, eigene_id=None):
    """Patientenakte. Mit eigene_id (Patientenkonto) nur lesend und nur für den eigenen Patienten."""
    st.title("Meine Akte" if eigene_id else "Patientenakte")
    zeige_flash()
    patienten = {p.patient_id: p for p in b.alle_patienten()}
    if not patienten:
        st.info("Noch keine Patienten. Lege unter „Patient anlegen“ den ersten an.")
        return
    if eigene_id:
        pid = eigene_id
    else:
        pid = st.selectbox("Patient", list(patienten), format_func=lambda i: name(patienten[i]), key="patient_wahl")
    p = patienten[pid]
    konto = None if eigene_id else b.konto_email_fuer(pid)
    st.caption(f"{alter(p.geburtsdatum)} Jahre, geboren am {p.geburtsdatum:%d.%m.%Y}"
               + (f", Patientenkonto: {konto}" if konto else ""))

    messungen = b.messungen(pid)
    letzte = {m.vitaltyp.bezeichnung: m for m in messungen}
    for col, typ in zip(st.columns(len(VITALTYPEN)), VITALTYPEN):
        m = letzte.get(typ)
        if m:
            kritisch = VITALTYPEN[typ][1].ist_kritisch(m.messwert.wert)
            col.metric(typ, f"{m.messwert.wert:g} {m.messwert.einheit}")
            col.caption("🔴 Außerhalb der Grenzen" if kritisch else "🟢 Im Normalbereich")

    tabs = st.tabs(["Vitalwerte", "Behandlungsverlauf"] + ([] if eigene_id else ["Erfassen"]))
    t1, t2 = tabs[0], tabs[1]
    with t1:
        if not messungen:
            st.info("Noch keine Messung vorhanden." if eigene_id else "Noch keine Messung. Erfasse sie im Tab „Erfassen“.")
        else:
            typ = st.radio("Messgröße", list(VITALTYPEN), horizontal=True, key="chart_typ")
            vital_chart(messungen, typ)
            st.caption("Grüner Bereich: Normalbereich. Gepunktete Linien: Grenzwerte.")
    with t2:
        verlauf = b.verlauf(pid)
        if not verlauf:
            st.info("Noch keine Behandlung dokumentiert.")
        else:
            st.dataframe(pd.DataFrame([{"Zeitpunkt": f"{v.zeitpunkt:%d.%m.%Y %H:%M}", "Maßnahme": v.massnahme,
                                        "Notiz": v.notiz} for v in reversed(verlauf)]),
                         hide_index=True, use_container_width=True)
    if not eigene_id:
        with tabs[2]:
            formulare_erfassen(b, pid, p)


def formulare_erfassen(b: MeditrackBackend, pid, p):
    links, rechts = st.columns(2)
    with links.form("messung"):
        st.subheader("Messung erfassen")
        typ = st.selectbox("Vitaltyp", list(VITALTYPEN), format_func=lambda t: f"{t} ({VITALTYPEN[t][0]})", key="mess_typ")
        regel = VITALTYPEN[typ][1]
        wert = st.number_input("Wert", value=float((regel.minimum + regel.maximum) / 2), step=0.1, key="mess_wert")
        if st.form_submit_button("Messung speichern"):
            try:
                _, warnung = b.messung_erfassen(pid, typ, wert)
            except ValueError as e:
                st.error(str(e))
            else:
                if warnung is None:
                    flash("success", "Messung gespeichert. Wert im Normalbereich.")
                else:
                    text = f"{name(p)}: {typ} {wert:g}, Grenze {warnung.schwellwert:g} ({warnung.schweregrad.value})"
                    gesendet = send_mail(f"Warnmeldung: {name(p)}", text)
                    flash("error", f"Warnmeldung erzeugt. {text}" + (" E-Mail gesendet." if gesendet else ""))
                st.rerun()
    with rechts.form("behandlung", clear_on_submit=True):
        st.subheader("Behandlung dokumentieren")
        massnahme = st.text_input("Maßnahme", key="beh_massnahme")
        notiz = st.text_area("Notiz", key="beh_notiz")
        if st.form_submit_button("Behandlung speichern"):
            try:
                b.behandlung_dokumentieren(pid, st.session_state["user"].benutzer_id, massnahme, notiz)
            except ValueError as e:
                st.error(str(e))
            else:
                flash("success", "Behandlung gespeichert.")
                st.rerun()


def seite_neuer_patient(b: MeditrackBackend):
    st.title("Patient anlegen")
    zeige_flash()
    with st.form("neuer_patient", clear_on_submit=True):
        c = st.columns(3)
        vorname = c[0].text_input("Vorname", key="pat_vorname")
        nachname = c[1].text_input("Nachname", key="pat_nachname")
        geb = c[2].date_input("Geburtsdatum", value=date(1970, 1, 1), min_value=date(1900, 1, 1), max_value=date.today(),
                              key="pat_geb")
        email = st.text_input("E-Mail-Adresse des Patienten", key="pat_email",
                              help="Daraus entsteht das Patientenkonto, über das der Patient seine Akte einsehen kann.")
        if st.form_submit_button("Patient speichern"):
            try:
                p, konto, pw = b.patient_mit_konto_anlegen(vorname, nachname, geb, email)
            except ValueError as e:
                st.error(str(e))
            else:
                flash("success", f"{name(p)} wurde angelegt. Zugang: {konto.email}, Initialpasswort `{pw}` "
                                 "(wird nur jetzt angezeigt, bitte dem Patienten sicher übergeben).")
                st.rerun()


def seite_alarme(b: MeditrackBackend):
    st.title("Warnmeldungen")
    patienten = {p.patient_id: p for p in b.alle_patienten()}
    log = b.alle_warnmeldungen()
    if not log:
        st.info("Noch keine Warnmeldungen aufgetreten.")
        return
    st.dataframe(pd.DataFrame([{
        "Zeitpunkt": f"{w.zeitpunkt:%d.%m.%Y %H:%M}", "Patient": name(patienten[w.patient_id]),
        "Messgröße": b.warn_vitaltyp.get(w.warnmeldung_id, ""), "Wert": w.aktueller_wert, "Grenze": w.schwellwert,
        "Schweregrad": SCHWERE[w.schweregrad.value], "Status": "bestätigt" if w.bestaetigt else "offen"} for w in log]),
        hide_index=True, use_container_width=True)
    with st.expander("Grenzwerte im Backend"):
        st.table(pd.DataFrame([{"Vitaltyp": t, "Einheit": e, "Minimum": r.minimum, "Maximum": r.maximum}
                               for t, (e, r) in VITALTYPEN.items()]))


# ---------------------------------------------------------------- Start
backend = get_backend()
if "user" not in st.session_state:
    seite_login(backend)
    st.stop()

user = st.session_state["user"]
with st.sidebar:
    st.header("🩺 MediTrack")
    st.caption(f"Angemeldet: {user.email} ({user.rolle.value.title()})")
    if st.button("Abmelden", key="logout"):
        st.session_state.clear()
        st.rerun()

if user.ist_patient:
    eigene_id = backend.patient_id_fuer(user)
    if eigene_id is None:
        st.title("Patientenbereich")
        st.info("Dein Konto ist noch keiner Patientenakte zugeordnet. Bitte wende dich an das Personal.")
    else:
        seite_patient(backend, eigene_id=eigene_id)
    st.stop()

with st.sidebar:
    seite = st.radio("Bereich", ["Stationsübersicht", "Patientenakte", "Patient anlegen", "Warnmeldungen"],
                     label_visibility="collapsed", key="nav")
    st.caption("Demo-Software, kein Medizinprodukt. Daten liegen nur im Arbeitsspeicher.")

{"Stationsübersicht": lambda: seite_uebersicht(backend), "Patientenakte": lambda: seite_patient(backend),
 "Patient anlegen": lambda: seite_neuer_patient(backend), "Warnmeldungen": lambda: seite_alarme(backend)}[seite]()
