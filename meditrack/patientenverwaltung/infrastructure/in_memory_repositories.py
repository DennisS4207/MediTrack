from uuid import UUID

from ..domain.model import Patient
from ..domain.repositories import PatientenRepository


class InMemoryPatientenRepository(PatientenRepository):

    def __init__(self):
        self.patienten = {}

    def speichern(self, patient: Patient) -> None:
        self.patienten[patient.patient_id] = patient

    def finde_nach_id(self, patient_id: UUID) -> Patient | None:
        return self.patienten.get(patient_id)