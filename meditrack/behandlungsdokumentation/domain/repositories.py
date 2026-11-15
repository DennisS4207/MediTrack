from abc import ABC, abstractmethod
from uuid import UUID

from .model import Behandlung


class BehandlungsRepository(ABC):

    @abstractmethod
    def speichern(self, behandlung: Behandlung) -> None:
        pass

    @abstractmethod
    def finde_nach_patient(self, patient_id: UUID) -> list[Behandlung]:
        """Alle Behandlungen des Patienten, älteste zuerst (neue Liste)."""
