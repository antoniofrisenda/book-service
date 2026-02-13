import logging
from bson import ObjectId
from fastapi import HTTPException, Response
from pkg.dto.book_dto import BookDto, InsertBook, UpdateBook
from pkg.factoty.book_factory import insert_to_model, model_to_dto, update_to_model
from pkg.repository.book_repo import BookRepository
from pkg.utils.validators import validate_and_format_isbn, validate_object_id


class BookService:

    def __init__(self, repository: BookRepository):
        self.repository = repository


    def create_book(self, insert_book: InsertBook) -> BookDto:
        logging.info(f"Creating new book: {insert_book.title}")

        if self.repository.collection.find_one({'isbn': insert_book.isbn}):
                raise HTTPException(status_code=401, detail="Duplicate ISBN!")
        
        
        insert_book.isbn = validate_and_format_isbn(insert_book.isbn)
        book = self.repository.create(insert_to_model(insert_book))
        
        if book is None:
            logging.error("Repository returned None for create_book")
            raise ValueError("Book creation failed")
        
        logging.info(f"Book created with ID: {book._id}")
        return model_to_dto(book)


    def get_book_by_Id(self, book_id: str) -> BookDto:
        logging.info(f"Searching book by ID: {book_id}")
        
        
        book_object_id = validate_object_id(book_id, "book ID")
        book = self.repository.find_by_Id(book_object_id)
        
        if book is None:
            logging.warning(f"Book not found with ID: {book_id}")
            raise HTTPException(status_code=404, detail="ID not found!")
        
        logging.info(f"Book found: ID={book_id}")
        return model_to_dto(book)


    def get_book_by_isbn(self, isbn: str) -> BookDto:
        logging.info(f"Searching book by ISBN: {isbn}")
        
        book_result = self.repository.find_by_Isbn(isbn)
        
        if book_result is None:
            logging.warning(f"Book not found with ISBN: {isbn}")
            raise HTTPException(status_code=404, detail="ISBN not found!")
        
        logging.info(f"Book found: ISBN={isbn}")
        return model_to_dto(book_result)


    def update_book_by_Id(self, book_id: str, update_book: UpdateBook) -> BookDto:
        logging.info(f"Updating book with ID: {book_id}")
        
        book_object_id = validate_object_id(book_id, "book ID")
        book = self.repository.find_by_Id(book_object_id)
        
        if book is None:
            logging.warning(f"Book to update not found: {book_id}")
            raise HTTPException(status_code=404, detail="ID not found!")
        
        new_book = update_to_model(book_id, update_book)
        book_updated = self.repository.update(book._id, new_book)
        
        if book_updated is None:
            logging.error(f"Repository returned None for update: {book_id}")
            raise ValueError("Book update failed")
        
        logging.info(f"Book updated successfully: ID={book_id}")
        return model_to_dto(book_updated)


    def delete_book_by_Id(self, id: str):
        book = self.get_book_by_Id(id)  
        
        book_deleted = self.repository.delete(ObjectId(book.id))
        
        if book_deleted is None:
            logging.warning(f"Deletion failed for ID: {id}")
            return Response(status_code=404)
        
        logging.info(f"Book deleted successfully: ID={id}")
        return Response(status_code=200)

