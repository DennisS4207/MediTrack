from datetime import datetime
from uuid import UUID, uuid4

from ..domain.model import Behandlung
from ..domain.repositories import BehandlungsRepository


class BehandlungsService:

    def __init__(self, repository: BehandlungsRepository):
        self.repository = repository

    def behandlung_dokumentieren(
        self,
        patient_id: UUID,
        mitarbeiter_id: UUID,
        massnahme: str,
        zeitpunkt: datetime | None = None,
        notiz: str = ""
    ) -> Behandlung:

        behandlung = Behandlung(
            behandlung_id=uuid4(),
            patient_id=patient_id,
            mitarbeiter_id=mitarbeiter_id,
            massnahme=massnahme,
            zeitpunkt=zeitpunkt or datetime.now(),
            notiz=notiz
        )

        self.repository.speichern(behandlung)

        return behandlung

    def verlauf_abrufen(self, patient_id: UUID) -> list[Behandlung]:
        return self.repository.finde_nach_patient(patient_id)
