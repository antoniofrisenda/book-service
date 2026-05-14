from dataclasses import dataclass, field
from bson import ObjectId
    
@dataclass
class Book:
    isbn: str
    title: str
    genre: str
    price: int
    author: str
    quotes: list[str] = field(default_factory=list)
    _id: ObjectId = field(default_factory = ObjectId) 
