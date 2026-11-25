"""Anbindung des Frontends an das MediTrack-Backend (Paket `meditrack`).

Das Backend ist eine reine Python-Bibliothek ohne HTTP-API und hält seine Daten in
In-Memory-Repositories. Dieses Modul verdrahtet deshalb die vorhandenen Services und
ergänzt, was im Backend noch leer ist (vitaldatenueberwachung: Service und Repository).
Am Backend-Code selbst wird nichts verändert.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from uuid import UUID, uuid4

from meditrack.alarmmanagement.application.alarm_service import AlarmService
from meditrack.alarmmanagement.domain.model import Schweregrad, Warnmeldung
from meditrack.alarmmanagement.infrastructure.in_memory_repositories import InMemoryWarnmeldungRepository
from meditrack.behandlungsdokumentation.application.behandlungs_service import BehandlungsService
from meditrack.behandlungsdokumentation.domain.model import Behandlung
from meditrack.behandlungsdokumentation.infrastructure.in_memory_repositories import InMemoryBehandlungsRepository
from meditrack.benutzerverwaltung.application.registrierungs_service import RegistrierungsService
from meditrack.benutzerverwaltung.domain.model import Benutzerkonto
from meditrack.benutzerverwaltung.infrastructure.in_memory_repositories import InMemoryBenutzerRepository
from meditrack.patientenverwaltung.application.patienten_service import PatientenService
from meditrack.patientenverwaltung.domain.model import Patient
from meditrack.patientenverwaltung.infrastructure.in_memory_repositories import InMemoryPatientenRepository
from meditrack.vitaldatenueberwachung.domain.model import Grenzwertregel, Messwert, Vitalmessung, Vitaltyp

# Vitaltyp: (Einheit, Grenzwertregel). Beispielwerte, medizinisch zu prüfen.
VITALTYPEN: dict[str, tuple[str, Grenzwertregel]] = {
    "Puls": ("bpm", Grenzwertregel(50, 120)),
    "Blutdruck systolisch": ("mmHg", Grenzwertregel(95, 160)),
    "Blutdruck diastolisch": ("mmHg", Grenzwertregel(55, 100)),
    "Sauerstoffsättigung": ("%", Grenzwertregel(92, 100)),
    "Temperatur": ("°C", Grenzwertregel(35.5, 38.0)),
}


def schweregrad_fuer(regel: Grenzwertregel, wert: float) -> Schweregrad:
    """Schweregrad nach Abstand zum Grenzwert, relativ zur Breite des Normbereichs.
    Das Backend legt das nicht fest, daher hier als nachvollziehbare Annahme."""
    abstand = max(regel.minimum - wert, wert - regel.maximum, 0)
    anteil = abstand / max(regel.maximum - regel.minimum, 1e-9)
    if anteil < 0.05:
        return Schweregrad.NIEDRIG
    if anteil < 0.15:
        return Schweregrad.MITTEL
    if anteil < 0.30:
        return Schweregrad.HOCH
    return Schweregrad.KRITISCH


class InMemoryVitalmessungRepository:
    """Ersatz für die noch leere Datei vitaldatenueberwachung/infrastructure."""

    def __init__(self):
        self.messungen: dict[UUID, Vitalmessung] = {}

    def speichern(self, messung: Vitalmessung) -> None:
        self.messungen[messung.messung_id] = messung

    def finde_nach_patient(self, patient_id: UUID) -> list[Vitalmessung]:
        return sorted((m for m in self.messungen.values() if m.patient_id == patient_id), key=lambda m: m.zeitpunkt)


def passwort_hash(passwort: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", passwort.encode(), salt, 200_000)
    return f"{salt.hex()}${digest.hex()}"


def passwort_pruefen(passwort: str, gespeichert: str) -> bool:
    try:
        salt_hex, _ = gespeichert.split("$", 1)
    except ValueError:
        return False
    return hmac.compare_digest(passwort_hash(passwort, bytes.fromhex(salt_hex)), gespeichert)


@dataclass
class MeditrackBackend:
    """Bündelt alle Services. Eine Instanz pro Prozess (siehe @st.cache_resource in app.py)."""

    patienten_repo: InMemoryPatientenRepository = field(default_factory=InMemoryPatientenRepository)
    warn_repo: InMemoryWarnmeldungRepository = field(default_factory=InMemoryWarnmeldungRepository)
    behandlungs_repo: InMemoryBehandlungsRepository = field(default_factory=InMemoryBehandlungsRepository)
    benutzer_repo: InMemoryBenutzerRepository = field(default_factory=InMemoryBenutzerRepository)
    vital_repo: InMemoryVitalmessungRepository = field(default_factory=InMemoryVitalmessungRepository)
    # Das Backend kennt keine Warnmeldung -> Vitaltyp-Zuordnung, daher hier gemerkt.
    warn_vitaltyp: dict[UUID, str] = field(default_factory=dict)
    # Das Backend verknüpft Konto und Patient nicht -> Benutzer-ID -> Patienten-ID, hier gemerkt.
    konto_patient: dict[UUID, UUID] = field(default_factory=dict)
    # Vom Personal hinterlegte E-Mail-Adresse je Patient (Patient-ID -> E-Mail, kleingeschrieben).
    patient_email: dict[UUID, str] = field(default_factory=dict)

    def __post_init__(self):
        self.patienten = PatientenService(self.patienten_repo)
        self.alarme = AlarmService(self.warn_repo)
        self.behandlungen = BehandlungsService(self.behandlungs_repo)
        self.registrierung = RegistrierungsService(self.benutzer_repo)

    # --- Benutzer -----------------------------------------------------------
    def registrieren(self, email: str, passwort: str, rolle: str) -> Benutzerkonto:
        if len(passwort) < 8:
            raise ValueError("Das Passwort muss mindestens 8 Zeichen lang sein")
        return self.registrierung.registrieren(email, passwort_hash(passwort), rolle)

    def anmelden(self, email: str, passwort: str) -> Benutzerkonto:
        konto = self.benutzer_repo.finde_nach_email(email.strip())
        if konto is None or not passwort_pruefen(passwort, konto.passwort_hash):
            raise ValueError("E-Mail oder Passwort ist falsch")
        return konto

    # --- Patienten ----------------------------------------------------------
    def patient_anlegen(self, vorname: str, nachname: str, geburtsdatum: date) -> Patient:
        return self.patienten.patient_anlegen(vorname, nachname, geburtsdatum)

    def patient_anlegen_mit_email(self, vorname: str, nachname: str, geburtsdatum: date, email: str) -> Patient:
        """Legt den Patienten an und hinterlegt seine E-Mail-Adresse. Mit dieser Adresse kann er sich
        anschließend selbst registrieren und wird dabei mit seiner Akte verknüpft."""
        email = (email or "").strip().lower()
        if not Benutzerkonto.EMAIL_REGEX.fullmatch(email):
            raise ValueError("Ungültige E-Mail-Adresse")
        if email in self.patient_email.values() or self.benutzer_repo.finde_nach_email(email) is not None:
            raise ValueError("E-Mail-Adresse ist bereits vergeben")
        patient = self.patient_anlegen(vorname, nachname, geburtsdatum)  # prüft Name und Geburtsdatum
        self.patient_email[patient.patient_id] = email
        return patient

    def patient_registrieren(self, email: str, passwort: str) -> Benutzerkonto:
        """Selbstregistrierung für Patienten. Es entsteht immer ein Konto mit der Rolle PATIENT,
        und nur, wenn das Personal zu dieser E-Mail-Adresse eine Patientenakte angelegt hat."""
        email = (email or "").strip().lower()
        patient_id = next((pid for pid, mail in self.patient_email.items() if mail == email), None)
        if patient_id is None:
            raise ValueError("Zu dieser E-Mail-Adresse gibt es keine Patientenakte. Bitte wende dich an das Personal.")
        if self.hat_konto(patient_id):
            raise ValueError("Für diese E-Mail-Adresse existiert bereits ein Konto")
        konto = self.registrieren(email, passwort, "PATIENT")
        self.konto_patient[konto.benutzer_id] = patient_id
        return konto

    def patient_id_fuer(self, konto: Benutzerkonto) -> UUID | None:
        """Patienten-ID, die zu einem Patientenkonto gehört (None, wenn keine Verknüpfung besteht)."""
        return self.konto_patient.get(konto.benutzer_id)

    def hat_konto(self, patient_id: UUID) -> bool:
        return patient_id in self.konto_patient.values()

    def alle_patienten(self) -> list[Patient]:
        # Das Repository-Interface hat keine Listenabfrage; die In-Memory-Implementierung schon.
        return sorted(self.patienten_repo.patienten.values(), key=lambda p: (p.nachname, p.vorname))

    # --- Vitaldaten ---------------------------------------------------------
    def messung_erfassen(self, patient_id: UUID, vitaltyp: str, wert: float,
                         zeitpunkt: datetime | None = None) -> tuple[Vitalmessung, Warnmeldung | None]:
        """Speichert die Messung und erzeugt bei Grenzwertverletzung automatisch eine Warnmeldung."""
        self.patienten.patient_abrufen(patient_id)  # wirft ValueError, wenn unbekannt
        einheit, regel = VITALTYPEN[vitaltyp]
        messung = Vitalmessung(uuid4(), patient_id, zeitpunkt or datetime.now(), Messwert(wert, einheit), Vitaltyp(vitaltyp))
        self.vital_repo.speichern(messung)
        if not regel.ist_kritisch(wert):
            return messung, None
        grenze = regel.minimum if wert < regel.minimum else regel.maximum
        warnung = self.alarme.warnmeldung_erzeugen(
            patient_id, wert, grenze, schweregrad_fuer(regel, wert), messung.zeitpunkt)
        self.warn_vitaltyp[warnung.warnmeldung_id] = vitaltyp
        return messung, warnung

    def messungen(self, patient_id: UUID) -> list[Vitalmessung]:
        return self.vital_repo.finde_nach_patient(patient_id)

    # --- Alarme -------------------------------------------------------------
    def offene_warnmeldungen(self, patient_id: UUID | None = None) -> list[Warnmeldung]:
        ids = [patient_id] if patient_id else [p.patient_id for p in self.alle_patienten()]
        offene = [w for pid in ids for w in self.alarme.offene_warnmeldungen(pid)]
        rang = {Schweregrad.KRITISCH: 0, Schweregrad.HOCH: 1, Schweregrad.MITTEL: 2, Schweregrad.NIEDRIG: 3}
        return sorted(offene, key=lambda w: (rang[w.schweregrad], -w.zeitpunkt.timestamp()))

    def alle_warnmeldungen(self) -> list[Warnmeldung]:
        return sorted(self.warn_repo.warnmeldungen.values(), key=lambda w: w.zeitpunkt, reverse=True)

    def warnung_bestaetigen(self, warnmeldung_id: UUID) -> Warnmeldung:
        return self.alarme.warnmeldung_bestaetigen(warnmeldung_id)

    # --- Behandlungen -------------------------------------------------------
    def behandlung_dokumentieren(self, patient_id: UUID, mitarbeiter_id: UUID, massnahme: str, notiz: str = "") -> Behandlung:
        self.patienten.patient_abrufen(patient_id)
        return self.behandlungen.behandlung_dokumentieren(patient_id, mitarbeiter_id, massnahme, notiz=notiz)

    def verlauf(self, patient_id: UUID) -> list[Behandlung]:
        return self.behandlungen.verlauf_abrufen(patient_id)


def demo_daten_laden(b: MeditrackBackend) -> Benutzerkonto:
    """Legt Demo-Konten, -Patienten, Messreihen und Behandlungen an. Liefert das Mitarbeiter-Konto."""
    pfleger = b.registrieren("pflege@meditrack.test", "demo-passwort", "MITARBEITER")
    basis = {"Puls": 74, "Blutdruck systolisch": 125, "Blutdruck diastolisch": 78, "Sauerstoffsättigung": 97, "Temperatur": 36.8}
    jetzt = datetime.now().replace(minute=0, second=0, microsecond=0)
    for i, (vn, nn, geb) in enumerate([("Helga", "Brandt", date(1948, 3, 12)), ("Karl", "Neumann", date(1957, 9, 30)),
                                       ("Sabine", "Roth", date(1971, 1, 22))]):
        if i == 0:  # Demo-Patientenkonto, verknüpft mit der ersten Akte
            p = b.patient_anlegen_mit_email(vn, nn, geb, "patient@meditrack.test")
            b.patient_registrieren("patient@meditrack.test", "demo-passwort")
        elif i == 1:  # E-Mail hinterlegt, noch nicht registriert: zum Ausprobieren der Registrierung
            p = b.patient_anlegen_mit_email(vn, nn, geb, "karl@meditrack.test")
        else:
            p = b.patient_anlegen(vn, nn, geb)
        for h in range(12, -1, -1):
            for typ, mittel in basis.items():
                wert = mittel + ((h * 7 + i * 3 + len(typ)) % 5 - 2) * (0.1 if typ == "Temperatur" else 1)
                if h == 0 and i == 1 and typ == "Sauerstoffsättigung":
                    wert = 86  # kritisch
                if h == 0 and i == 2 and typ == "Puls":
                    wert = 128  # leicht über Grenze
                b.messung_erfassen(p.patient_id, typ, round(min(wert, 100) if typ == "Sauerstoffsättigung" else wert, 1),
                                   jetzt - timedelta(hours=2 * h))
        b.behandlung_dokumentieren(p.patient_id, pfleger.benutzer_id, "Aufnahmegespräch und Erstuntersuchung")
    return pfleger
