from datetime import datetime
from uuid import UUID, uuid4

from ..domain.model import Schweregrad, Warnmeldung
from ..domain.repositories import WarnmeldungRepository


class AlarmService:

    def __init__(self, repository: WarnmeldungRepository):
        self.repository = repository

    def warnmeldung_erzeugen(
        self,
        patient_id: UUID,
        aktueller_wert: float,
        schwellwert: float,
        schweregrad: Schweregrad | str,
        zeitpunkt: datetime | None = None
    ) -> Warnmeldung:

        warnmeldung = Warnmeldung(
            warnmeldung_id=uuid4(),
            patient_id=patient_id,
            aktueller_wert=aktueller_wert,
            schwellwert=schwellwert,
            schweregrad=schweregrad,
            zeitpunkt=zeitpunkt or datetime.now()
        )

        self.repository.speichern(warnmeldung)

        return warnmeldung

    def warnmeldung_abrufen(self, warnmeldung_id: UUID) -> Warnmeldung:

        warnmeldung = self.repository.finde_nach_id(warnmeldung_id)

        if warnmeldung is None:
            raise ValueError("Warnmeldung wurde nicht gefunden")

        return warnmeldung

    def warnmeldung_bestaetigen(self, warnmeldung_id: UUID) -> Warnmeldung:

        bestaetigt = self.warnmeldung_abrufen(warnmeldung_id).als_bestaetigt()

        self.repository.speichern(bestaetigt)

        return bestaetigt

    def offene_warnmeldungen(self, patient_id: UUID) -> list[Warnmeldung]:
        return self.repository.finde_offene_nach_patient(patient_id)
