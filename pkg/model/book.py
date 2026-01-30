from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4

class BookCreated(BaseModel):
    title: str
    genre: str
    author: str
    isbn: str
    quotes: list[str] = Field(default_factory=list)
    
    @classmethod
    def from_mongo(cls, doc):
        doc['id'] = doc.pop('_id')  
        return cls(**doc)


class Book(BaseModel):
    title: str
    genre: str
    author: str
    isbn: str
    id: UUID = Field(default_factory=uuid4, alias="_id")
    quotes: list[str] = Field(default_factory=list)
    
    model_config = ConfigDict(
        populate_by_name=True,  
        json_encoders={UUID: str}
    )
    
    @classmethod
    def from_mongo(cls, doc):
        doc['id'] = doc.pop('_id')  
        return cls(**doc)
