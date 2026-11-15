from uuid import UUID

from ..domain.model import Warnmeldung
from ..domain.repositories import WarnmeldungRepository


class InMemoryWarnmeldungRepository(WarnmeldungRepository):

    def __init__(self):
        self.warnmeldungen: dict[UUID, Warnmeldung] = {}

    def speichern(self, warnmeldung: Warnmeldung) -> None:
        self.warnmeldungen[warnmeldung.warnmeldung_id] = warnmeldung

    def finde_nach_id(self, warnmeldung_id: UUID) -> Warnmeldung | None:
        return self.warnmeldungen.get(warnmeldung_id)

    def finde_offene_nach_patient(self, patient_id: UUID) -> list[Warnmeldung]:
        offene = (
            w for w in self.warnmeldungen.values()
            if w.patient_id == patient_id and not w.bestaetigt
        )
        return sorted(offene, key=lambda w: w.zeitpunkt)
