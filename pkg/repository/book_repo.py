from dataclasses import asdict
from bson import ObjectId
from loguru import logger
from pymongo import ASCENDING
from pkg.config.mogodb import MongoConnection
from pkg.model.book import Book



class BookRepository:

    def __init__(self, mongo_connection: MongoConnection):
        self.collection = mongo_connection.database.books
        self.collection.create_index([('isbn', ASCENDING)], unique = True, name= "isbn_unique")
    
        
    def create(self, book: Book) -> Book:
        try:
            result = self.collection.insert_one(asdict(book))
            
            book._id  = result.inserted_id
            return book
        
        except Exception as e:
            logger.error(f"Error with book creation: {e}")
            raise
    
    
    
    def find_by_Id(self, book_id: ObjectId) -> Book | None:
        
        try: 
            raw_book = self.collection.find_one({'_id': book_id})
            
            if raw_book is None:
                return None
            
            return Book(**raw_book)
        except Exception as e:
            logger.error(f"Error with the research of this book ID: {book_id}: {e}")
            logger.exception("Full detail of error: ")
            raise
    
    
    def find_by_Isbn(self, isbn: str) -> Book | None:
        
        try:
            result = self.collection.find_one({'isbn' : isbn})
            
            if result is None:
                return None
            return Book(**result)
        
        except Exception as e:
            logger.error(f"Error with the research of this book isbn: {isbn}: {e}")
            logger.exception("Full detail of error:")
            raise
    
     
        
    def update(self, book_id: ObjectId, update_book: Book) -> Book | None:
        try:
            result = self.collection.replace_one({'_id': book_id}, asdict(update_book))
            
            if result.matched_count == 0:
                return None
            
            return update_book
            
        except Exception as e:
            logger.error(f"Error with book update: {e}")
            logger.exception("Full detail of error:")   
            raise

    
        
    def delete(self, deleted_id: ObjectId) -> bool:
        try:
            result = self.collection.delete_one({'_id': deleted_id})
            
            if result.deleted_count == 0:
                return False

            return True
            
        except Exception as e:
            logger.error(f"Error deleting book with ID {deleted_id}: {e}")
            logger.exception("Full detail of error:")
            raise
