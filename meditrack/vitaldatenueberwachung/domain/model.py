from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Messwert:
    wert: float
    einheit: str

    def __post_init__(self):
        if not isfinite(self.wert):
            raise ValueError("Ungültiger Messwert")

        if not self.einheit.strip():
            raise ValueError("Einheit darf nicht leer sein")

@dataclass(frozen=True)
class Grenzwertregel:
    minimum: float
    maximum: float

    def __post_init__(self):
        if not isfinite(self.minimum) or not isfinite(self.maximum):
            raise ValueError("Grenzwerte müssen endlich sein")

        if self.minimum > self.maximum:
            raise ValueError(
                "Minimum darf nicht größer als Maximum sein"
            )

    def ist_kritisch(self, wert: float) -> bool:
        if not isfinite(wert):
            raise ValueError("Ungültiger Vitalwert")

        return wert < self.minimum or wert > self.maximum
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Vitaltyp:
    bezeichnung: str

    def __post_init__(self):
        if not isinstance(self.bezeichnung, str):
            raise ValueError("Vitaltyp muss ein Text sein")

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
            raise ValueError("Ungültige Messungs-ID")

        if not isinstance(self.patient_id, UUID):
            raise ValueError("Ungültige Patienten-ID")

        if not isinstance(self.zeitpunkt, datetime):
            raise ValueError("Ungültiger Zeitpunkt")

        if not isinstance(self.messwert, Messwert):
            raise ValueError("Ungültiger Messwert")

        if not isinstance(self.vitaltyp, Vitaltyp):
            raise ValueError("Ungültiger Vitaltyp")