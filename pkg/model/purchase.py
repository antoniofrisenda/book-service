from dataclasses import dataclass, field
from datetime import datetime
from bson import ObjectId


@dataclass
class Purchase:
    user_id: str
    book_id: str
    total: float
    created_at: datetime
    _id: ObjectId = field(default_factory=ObjectId)
