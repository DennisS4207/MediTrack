
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar
from uuid import UUID
import re


class Benutzerrolle(str, Enum):
    PATIENT = "PATIENT"
    MITARBEITER = "MITARBEITER"


@dataclass(frozen=True, slots=True)
class Benutzerkonto:
    benutzer_id: UUID
    email: str
    passwort_hash: str = field(repr=False)
    rolle: Benutzerrolle

    EMAIL_REGEX: ClassVar[re.Pattern[str]] = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    def __post_init__(self):
        if not isinstance(self.benutzer_id, UUID):
            raise ValueError("Ungültige Benutzer-ID")

        if not isinstance(self.email, str):
            raise ValueError("E-Mail muss ein Text sein")

        if not self.EMAIL_REGEX.fullmatch(self.email):
            raise ValueError("Ungültige E-Mail-Adresse")

        if (
            not isinstance(self.passwort_hash, str)
            or not self.passwort_hash.strip()
        ):
            raise ValueError("Passwort-Hash darf nicht leer sein")

        if not isinstance(self.rolle, Benutzerrolle):
            raise ValueError("Ungültige Benutzerrolle")

    @property
    def ist_patient(self) -> bool:
        return self.rolle == Benutzerrolle.PATIENT
