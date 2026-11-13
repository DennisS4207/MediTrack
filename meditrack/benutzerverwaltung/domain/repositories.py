from abc import ABC, abstractmethod
from .model import Benutzerkonto


class BenutzerRepository(ABC):

    @abstractmethod
    def speichern(self, konto: Benutzerkonto) -> None:
        pass

    @abstractmethod
    def finde_nach_email(self, email: str) -> Benutzerkonto | None:
        pass