from typing import List, Optional
from uuid import UUID
from pymongo import MongoClient
from fastapi import HTTPException
from pkg.model.book import Book, BookCreated





class BookRepository:

    def __init__(self, string_connection: str, db_name: str):
        self.client = MongoClient(string_connection, uuidRepresentation='standard')
        self.db = self.client[db_name]
        self.collection = self.db['books']
    
        
    def create(self, book_create: BookCreated) -> Book:
        book = Book(**book_create.model_dump())
        
        book_dict = book.model_dump(by_alias=True, mode='python')
        self.collection.insert_one(book_dict)
        
        return book
    
    
    def find_by_Id(self, book_id: str) -> Optional[Book]:
        
        result = self.collection.find_one({'_id': UUID(book_id)})
        
        if result is None:
            raise HTTPException(status_code =404, detail= "Libro non trovato!")
        
        return Book.from_mongo(result)
    
        
    def find_by_author(self, author:str) -> List[Book]:
        
        results = self.collection.find({'author': {'$regex': author, '$options': 'i'}})
        
        return [Book.from_mongo(doc) for doc in results]
    
        
    def find_book_by_quote(self, search_text_quote: str) -> List[Book]:
   
        result = self.collection.find({
        'quotes': {'$regex': search_text_quote, '$options': 'i'}
        })
    
        return [Book.from_mongo(doc) for doc in result]
    
    
        
    def find_by_genre(self, genre: str) -> List[Book]:
        
        results = self.collection.find({'genre':{'$regex' : genre,'$options': 'i' }})
        
        return [Book.from_mongo(doc) for doc in results]
        
    
    
    def find_by_Isbn(self, isbn: str) -> Optional[Book]:
        result = self.collection.find_one({'isbn' : isbn})
        
        if result is None:
            return None
        
        return Book(**result)
    
     
        
    def update(self, book_id: str, update_book: BookCreated) -> Optional[Book]:
    
   
        existing = self.find_by_Id(book_id)
        if not existing:
            return None
        
        
        result = self.collection.update_one(
            {'_id': UUID(book_id)}, 
            {'$set': update_book.model_dump(exclude_unset=True)}  
        )
        
        if result.modified_count > 0:
            return self.find_by_Id(book_id)
        
        return existing
    
        
    def delete(self, book_id: str) -> bool:
        result = self.collection.find_one_and_delete({'_id': UUID(book_id)})
    
        if result is None:
            raise HTTPException(status_code=404, detail="Libro non trovato!")
        
        return True
    
    