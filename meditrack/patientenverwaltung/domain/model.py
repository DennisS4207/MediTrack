from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID


@dataclass
class Patient:
    patient_id: UUID
    vorname: str
    nachname: str
    geburtsdatum: date

    def __post_init__(self):
        if not isinstance(self.patient_id, UUID):
            raise ValueError("Ungültige Patienten-ID")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        if not isinstance(self.vorname, str) or not self.vorname.strip():
            raise ValueError("Vorname darf nicht leer sein")

        if not isinstance(self.nachname, str) or not self.nachname.strip():
            raise ValueError("Nachname darf nicht leer sein")

        # datetime erbt von date, ist als Geburtsdatum aber nicht vergleichbar -> vorab abweisen
        if not isinstance(self.geburtsdatum, date) or isinstance(self.geburtsdatum, datetime):
            raise ValueError("Ungültiges Geburtsdatum")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        if self.geburtsdatum > date.today():
            raise ValueError("Geburtsdatum darf nicht in der Zukunft liegen")
