from dataclasses import dataclass
from datetime import date


@dataclass
class AuthorDto:
    id: str
    name: str
    birthDate: date
    biography: str


@dataclass
class InsertAuthor:
    name: str
    birthDate: date
    biography: str
