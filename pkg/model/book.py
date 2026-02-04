from dataclasses import dataclass, field
from bson import ObjectId
    
@dataclass
class Book:
    title: str
    genre: str
    author: str
    isbn: str
    quotes: list[str] = field(default_factory=list)
    _id: ObjectId = field(default_factory = ObjectId) 
