from ..domain.model import Benutzerkonto
from ..domain.repositories import BenutzerRepository


class InMemoryBenutzerRepository(BenutzerRepository):

    def __init__(self):
        self.benutzer = {}

    def speichern(self, konto: Benutzerkonto) -> None:
        self.benutzer[konto.email] = konto

    def finde_nach_email(self, email: str) -> Benutzerkonto | None:
        return self.benutzer.get(email)