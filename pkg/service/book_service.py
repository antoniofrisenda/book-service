from bson import ObjectId
from fastapi import HTTPException, Response
from pkg.dto.book_dto import BookDto, InsertBook, UpdateBook
from pkg.factoty.book_factory import insert_to_model, model_to_dto, update_to_model
from pkg.repository.book_repo import BookRepository


class BookService:

    def __init__(self, repository: BookRepository):
        self.repository = repository

    def create_book(self, insert_book: InsertBook) -> BookDto:
        try:
            book = self.repository.create(insert_to_model(insert_book))
        except Exception as e:
            raise RuntimeError(f"Request failed: create_book -> {type(e).__name__}: {e}")

        if book is None:
            raise RuntimeError("Something went wrong: create_book returned None")

        return model_to_dto(book)

    def get_book_by_Id(self, book_id: str) -> BookDto:
        try:
            book = self.repository.find_by_Id(ObjectId(book_id))
        except Exception as e:
            raise RuntimeError(f"Request failed: get_book_by_Id({book_id}) -> {type(e).__name__}: {e}")

        if book is None:
            raise HTTPException(status_code=404, detail="ID not found!")  # raise, non return [web:84]

        return model_to_dto(book)
    

    def get_book_by_isbn(self, isbn: str) -> BookDto:
        try:
            book_result = self.repository.find_by_Isbn(isbn)
        except Exception as e:
            raise RuntimeError(f"Request failed: get_book_by_isbn({isbn}) -> {type(e).__name__}: {e}")

        if book_result is None:
            raise HTTPException(status_code=404, detail="ISBN not found!")  # raise, non return [web:84]

        return model_to_dto(book_result)
    

    def update_book_by_Id(self, book_id: str, update_book: UpdateBook) -> BookDto:
        try:
            book = self.repository.find_by_Id(ObjectId(book_id))
        except Exception as e:
            raise RuntimeError(f"Request failed: update_book_by_Id find_by_Id({book_id}) -> {type(e).__name__}: {e}")

        if book is None:
            raise HTTPException(status_code=404, detail="ID nto found!")

        try:
            new_book = update_to_model(book_id, update_book)
        except Exception as e:
            raise RuntimeError(f"Request failed: update_book_by_Id update_to_model({book_id}) -> {type(e).__name__}: {e}")

        try:
            book_updated = self.repository.update(book._id, new_book)
        except Exception as e:
            raise RuntimeError(f"Request failed: update_book_by_Id update({book._id}) -> {type(e).__name__}: {e}")

        if book_updated is None:
            raise RuntimeError(f"Something went wrong: update_book_by_Id({book_id}) returned None")

        return model_to_dto(book_updated)



    def delete_book_by_Id(self, id: str):
        try:
            book = self.get_book_by_Id(id)
            
        except Exception as e:
            raise RuntimeError(f"Request failed: deleted_book_by_id find_by_id ({id}) -> {type(e).__name__}: {e}")
        
        if book is None:
            raise HTTPException(status_code=404, detail="ID not found!")
        
        try:
            book_deleted = self.repository.delete(ObjectId(book.id))
        except Exception as e:
            raise RuntimeError(f"Request failed: delete_book_by_Id({book.id}) -> {type(e).__name__}: {e}")

        if book_deleted is None:
            return Response(status_code=404)

        return Response(status_code=200)
