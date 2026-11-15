from ..domain.model import Benutzerkonto
from ..domain.repositories import BenutzerRepository


class InMemoryBenutzerRepository(BenutzerRepository):

    def __init__(self):
        self.benutzer: dict[str, Benutzerkonto] = {}

    @staticmethod
    def _schluessel(email: str) -> str:
        # E-Mail-Adressen werden ohne Beachtung der Groß-/Kleinschreibung verglichen
        return email.lower()

    def speichern(self, konto: Benutzerkonto) -> None:
        self.benutzer[self._schluessel(konto.email)] = konto

    def finde_nach_email(self, email: str) -> Benutzerkonto | None:
        return self.benutzer.get(self._schluessel(email))
