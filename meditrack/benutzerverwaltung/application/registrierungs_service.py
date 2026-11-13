from uuid import uuid4

from ..domain.model import Benutzerkonto
from ..domain.repositories import BenutzerRepository


class RegistrierungsService:

    def __init__(self, repository: BenutzerRepository):
        self.repository = repository

    def registrieren(
        self,
        email: str,
        passwort_hash: str,
        rolle: str
    ) -> Benutzerkonto:

        if self.repository.finde_nach_email(email) is not None:
            raise ValueError("E-Mail-Adresse ist bereits registriert")

        konto = Benutzerkonto(
            benutzer_id=uuid4(),
            email=email,
            passwort_hash=passwort_hash,
            rolle=rolle
        )

        self.repository.speichern(konto)

        return konto