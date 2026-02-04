from dataclasses import asdict
from typing import List, Optional
from bson import ObjectId
from pymongo import ASCENDING
from pkg.config.mogodb import MongoConnection
from pkg.model.book import Book



class BookRepository:

    def __init__(self, mongo_connection: MongoConnection):
        self.collection = mongo_connection.database.books
        self.collection.create_index([('isbn', ASCENDING)], unique = True, name= "isbn_unique")
    
        
    def create(self, book: Book) -> Book:
        result = self.collection.insert_one(asdict(book))
        
        book._id  = result.inserted_id
        return book
    
    
    def find_by_Id(self, book_id: ObjectId) -> Optional[Book]:
        raw_book = self.collection.find_one({'_id': ObjectId(book_id)})
        
        if raw_book is None:
            return None
        
        return Book(**raw_book)
        
    
        
    def find_by_author(self, author:str) -> List[Book]:
        # TO-DO : spostare su opensearch
        results = self.collection.find({'author': {'$regex': author, '$options': 'i'}})
        
        
        
        
        
    def find_book_by_quote(self, search_text_quote: str) -> List[Book]:
        # TO-DO : spostare su opensearch
        result = self.collection.find({
        'quotes': {'$regex': search_text_quote, '$options': 'i'}
        })
    
        return [Book.from_doc(doc) for doc in result]

    
        
    def find_by_genre(self, genre: str) -> List[Book]:
        # TO-DO : spostare su opensearch
        results = self.collection.find({'genre':{'$regex' : genre,'$options': 'i' }})
        
        return [Book.from_mongo(doc) for doc in results]
        
    
    
    def find_by_Isbn(self, isbn: str) -> Optional[Book]:
        result = self.collection.find_one({'isbn' : isbn})
        
        if result is None:
            return None
        
        return Book(**result)
    
     
        
    def update(self, book_id: ObjectId, update_book: Book) -> Book:
    
        self.collection.replace_one({'_id' : book_id}, asdict(update_book))
        
        return update_book
        
    
        
    def delete(self, book : Book) -> bool:
        
        result = self.collection.delete_one({'_id' : book._id})
        
        return result.deleted_count == 1