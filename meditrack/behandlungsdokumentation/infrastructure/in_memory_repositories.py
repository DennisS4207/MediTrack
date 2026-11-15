from uuid import UUID

from ..domain.model import Behandlung
from ..domain.repositories import BehandlungsRepository


class InMemoryBehandlungsRepository(BehandlungsRepository):

    def __init__(self):
        self.behandlungen: dict[UUID, Behandlung] = {}

    def speichern(self, behandlung: Behandlung) -> None:
        self.behandlungen[behandlung.behandlung_id] = behandlung

    def finde_nach_patient(self, patient_id: UUID) -> list[Behandlung]:
        eigene = (b for b in self.behandlungen.values() if b.patient_id == patient_id)
        return sorted(eigene, key=lambda b: b.zeitpunkt)
