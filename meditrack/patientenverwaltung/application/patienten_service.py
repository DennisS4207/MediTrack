from datetime import date
from uuid import UUID, uuid4

from ..domain.model import Patient
from ..domain.repositories import PatientenRepository


class PatientenService:

    def __init__(self, repository: PatientenRepository):
        self.repository = repository

    def patient_anlegen(
        self,
        vorname: str,
        nachname: str,
        geburtsdatum: date
    ) -> Patient:

        patient = Patient(
            patient_id=uuid4(),
            vorname=vorname,
            nachname=nachname,
            geburtsdatum=geburtsdatum
        )

        self.repository.speichern(patient)

        return patient

    def patient_abrufen(self, patient_id: UUID) -> Patient:

        patient = self.repository.finde_nach_id(patient_id)

        if patient is None:
            raise ValueError("Patient wurde nicht gefunden")

        return patient