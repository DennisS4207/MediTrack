from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum
from math import isfinite
from uuid import UUID


class Schweregrad(str, Enum):
    NIEDRIG = "NIEDRIG"
    MITTEL = "MITTEL"
    HOCH = "HOCH"
    KRITISCH = "KRITISCH"


def _ist_endliche_zahl(wert: object) -> bool:
    """Prüft, ob wert eine endliche int/float-Zahl ist (bool zählt nicht als Zahl)."""
    if isinstance(wert, bool) or not isinstance(wert, (int, float)):
        return False

    try:
        return isfinite(wert)
    except OverflowError:  # Ganzzahlen, die größer als float sind
        return False


@dataclass(frozen=True)
class Warnmeldung:
    warnmeldung_id: UUID
    patient_id: UUID
    aktueller_wert: float
    schwellwert: float
    schweregrad: Schweregrad
    zeitpunkt: datetime
    bestaetigt: bool = False

    def __post_init__(self):
        if not isinstance(self.warnmeldung_id, UUID):
            raise ValueError("Ungültige Warnmeldungs-ID")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        if not isinstance(self.patient_id, UUID):
            raise ValueError("Ungültige Patienten-ID")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        if not _ist_endliche_zahl(self.aktueller_wert):
            raise ValueError("Ungültiger aktueller Wert")

        if not _ist_endliche_zahl(self.schwellwert):
            raise ValueError("Ungültiger Schwellwert")

        # Text ("HOCH") wird in das Enum umgewandelt; unbekannte Werte -> ValueError.
        # Das Objekt ist frozen, daher object.__setattr__ statt normaler Zuweisung.
        try:
            object.__setattr__(self, "schweregrad", Schweregrad(self.schweregrad))
        except ValueError:
            raise ValueError("Ungültiger Schweregrad") from None

        if not isinstance(self.zeitpunkt, datetime):
            raise ValueError("Ungültiger Zeitpunkt")  # noqa: TRY004 (Domänenvalidierung wirft bewusst ValueError)

        # Mit Zeitzone des Zeitpunkts vergleichen, sonst TypeError bei naiv/aware-Mischung
        if self.zeitpunkt > datetime.now(self.zeitpunkt.tzinfo):
            raise ValueError("Zeitpunkt darf nicht in der Zukunft liegen")

    def als_bestaetigt(self) -> "Warnmeldung":
        """Liefert eine bestätigte Kopie; das Original bleibt unverändert."""
        return replace(self, bestaetigt=True)
