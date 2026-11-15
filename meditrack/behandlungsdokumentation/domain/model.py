from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Behandlung:
    behandlung_id: UUID
    patient_id: UUID
    mitarbeiter_id: UUID
    massnahme: str
    zeitpunkt: datetime
    notiz: str = ""

    def __post_init__(self):
        if not isinstance(self.behandlung_id, UUID):
            raise ValueError("Ungültige Behandlungs-ID")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        if not isinstance(self.patient_id, UUID):
            raise ValueError("Ungültige Patienten-ID")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        if not isinstance(self.mitarbeiter_id, UUID):
            raise ValueError("Ungültige Mitarbeiter-ID")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        if self.patient_id == self.mitarbeiter_id:
            raise ValueError("Patient und Mitarbeiter dürfen nicht dieselbe ID haben")

        if not isinstance(self.massnahme, str) or not self.massnahme.strip():
            raise ValueError("Maßnahme darf nicht leer sein")

        if not isinstance(self.notiz, str):
            raise ValueError("Notiz muss ein Text sein")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        if not isinstance(self.zeitpunkt, datetime):
            raise ValueError("Ungültiger Zeitpunkt")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        # Mit Zeitzone des Zeitpunkts vergleichen, sonst TypeError bei naiv/aware-Mischung
        if self.zeitpunkt > datetime.now(self.zeitpunkt.tzinfo):
            raise ValueError("Zeitpunkt darf nicht in der Zukunft liegen")
