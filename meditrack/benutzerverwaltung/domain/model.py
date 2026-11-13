from dataclasses import dataclass
from uuid import UUID
import re


@dataclass(frozen=True)
class Benutzerkonto:
    benutzer_id: UUID
    email: str
    passwort_hash: str
    rolle: str

    def __post_init__(self):
        if not isinstance(self.benutzer_id, UUID):
            raise ValueError("Ungültige Benutzer-ID")

        if not isinstance(self.email, str):
            raise ValueError("E-Mail muss ein Text sein")

        email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(email_regex, self.email):
            raise ValueError("Ungültige E-Mail-Adresse")

        if not isinstance(self.passwort_hash, str) or not self.passwort_hash.strip():
            raise ValueError("Passwort-Hash darf nicht leer sein")

        if self.rolle not in ("PATIENT", "MITARBEITER"):
            raise ValueError("Ungültige Benutzerrolle")


