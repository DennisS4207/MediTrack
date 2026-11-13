from abc import ABC, abstractmethod
from uuid import UUID

from .model import Patient


class PatientenRepository(ABC):

    @abstractmethod
    def speichern(self, patient: Patient) -> None:
        pass

    @abstractmethod
    def finde_nach_id(self, patient_id: UUID) -> Patient | None:
        pass