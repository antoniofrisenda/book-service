from dataclasses import dataclass, field


@dataclass
class BookDto:
    id: str
    title: str
    genre: str 
    author: str 
    isbn: str
    quotes: list[str] = field(default_factory=list)


@dataclass
class InsertBook:
    title: str
    genre: str
    author: str
    isbn: str
    quotes: list[str] = field(default_factory=list)


@dataclass
class UpdateBook:
    title: str
    genre: str
    author: str
    isbn: str
    quotes: list[str] = field(default_factory=list)
    


    
