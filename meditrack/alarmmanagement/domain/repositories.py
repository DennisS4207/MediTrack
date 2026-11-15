from abc import ABC, abstractmethod
from uuid import UUID

from .model import Warnmeldung


class WarnmeldungRepository(ABC):

    @abstractmethod
    def speichern(self, warnmeldung: Warnmeldung) -> None:
        pass

    @abstractmethod
    def finde_nach_id(self, warnmeldung_id: UUID) -> Warnmeldung | None:
        pass

    @abstractmethod
    def finde_offene_nach_patient(self, patient_id: UUID) -> list[Warnmeldung]:
        """Unbestätigte Warnmeldungen des Patienten, älteste zuerst."""
