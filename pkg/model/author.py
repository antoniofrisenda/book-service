from dataclasses import dataclass, field
from datetime import date
from bson import ObjectId


@dataclass
class Author:
    name: str
    birth_date: date
    biography: str
    _id: ObjectId = field(default_factory=ObjectId)
