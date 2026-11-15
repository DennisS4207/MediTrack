from dataclasses import dataclass
from datetime import datetime
from math import isfinite
from uuid import UUID


def _ist_endliche_zahl(wert: object) -> bool:
    """Prüft, ob wert eine endliche int/float-Zahl ist (bool zählt nicht als Zahl)."""
    if isinstance(wert, bool) or not isinstance(wert, (int, float)):
        return False

    try:
        return isfinite(wert)
    except OverflowError:  # Ganzzahlen, die größer als float sind
        return False


@dataclass(frozen=True)
class Messwert:
    wert: float
    einheit: str

    def __post_init__(self):
        if not _ist_endliche_zahl(self.wert):
            raise ValueError("Ungültiger Messwert")

        if not isinstance(self.einheit, str) or not self.einheit.strip():
            raise ValueError("Einheit darf nicht leer sein")


@dataclass(frozen=True)
class Grenzwertregel:
    minimum: float
    maximum: float

    def __post_init__(self):
        if not (_ist_endliche_zahl(self.minimum) and _ist_endliche_zahl(self.maximum)):
            raise ValueError("Grenzwerte müssen endlich sein")

        if self.minimum > self.maximum:
            raise ValueError(
                "Minimum darf nicht größer als Maximum sein"
            )

    def ist_kritisch(self, wert: float) -> bool:
        if not _ist_endliche_zahl(wert):
            raise ValueError("Ungültiger Vitalwert")

        return not self.minimum <= wert <= self.maximum


@dataclass(frozen=True)
class Vitaltyp:
    bezeichnung: str

    def __post_init__(self):
        if not isinstance(self.bezeichnung, str):
            raise ValueError("Vitaltyp muss ein Text sein")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        if not self.bezeichnung.strip():
            raise ValueError("Vitaltyp darf nicht leer sein")


@dataclass(frozen=True)
class Vitalmessung:
    messung_id: UUID
    patient_id: UUID
    zeitpunkt: datetime
    messwert: Messwert
    vitaltyp: Vitaltyp

    def __post_init__(self):
        if not isinstance(self.messung_id, UUID):
            raise ValueError("Ungültige Messungs-ID")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        if not isinstance(self.patient_id, UUID):
            raise ValueError("Ungültige Patienten-ID")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        if not isinstance(self.zeitpunkt, datetime):
            raise ValueError("Ungültiger Zeitpunkt")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        if not isinstance(self.messwert, Messwert):
            raise ValueError("Ungültiger Messwert")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        if not isinstance(self.vitaltyp, Vitaltyp):
            raise ValueError("Ungültiger Vitaltyp")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)
