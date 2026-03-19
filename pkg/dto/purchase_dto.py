from dataclasses import dataclass
from datetime import datetime


@dataclass
class PurchaseDto:
    id: str
    userId: str
    bookId: str
    total: float
    createdAt: datetime


@dataclass
class InsertPurchase:
    userId: str
    bookId: str
