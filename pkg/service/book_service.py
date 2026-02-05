from bson import ObjectId
from fastapi import HTTPException, Response
from pkg.dto.book_dto import BookDto, InsertBook, UpdateBook
from pkg.factoty.book_factory import model_to_dto, update_to_model
from pkg.model.book import Book
from pkg.repository.book_repo import BookRepository


class BookService:

    def __init__(self, repository: BookRepository):
        self.repository = repository

    def create_book(self, insert_book: InsertBook) -> BookDto:
        try:
            book = self.repository.create(insert_book)
        except Exception as e:
            raise RuntimeError(f"Request failed: create_book -> {type(e).__name__}: {e}")

        if book is None:
            raise RuntimeError("Something went wrong: create_book returned None")

        return model_to_dto(book)

    def get_book_by_Id(self, book_id: str) -> BookDto:
        try:
            book = self.repository.find_by_Id(book_id)
        except Exception as e:
            raise RuntimeError(f"Request failed: get_book_by_Id({book_id}) -> {type(e).__name__}: {e}")

        if book is None:
            raise HTTPException(status_code=404, detail="ID non trovato!")  # raise, non return [web:84]

        return model_to_dto(book)

    def get_book_by_author(self, author: str) -> list[Book]:
        # TO-DO : spostare su opensearch
        finded_books = self.repository.find_by_author(author)
        return finded_books

    def get_book_by_genre(self, genre: str) -> list[Book]:
        # TO-DO : spostare su opensearch
        list_finded_book = self.repository.find_by_genre(genre)
        return list_finded_book

    def get_book_by_isbn(self, isbn: str) -> BookDto:
        try:
            book_result = self.repository.find_by_Isbn(isbn)
        except Exception as e:
            raise RuntimeError(f"Request failed: get_book_by_isbn({isbn}) -> {type(e).__name__}: {e}")

        if book_result is None:
            raise HTTPException(status_code=404, detail="ISBN non trovato!")  # raise, non return [web:84]

        return model_to_dto(book_result)

    def get_books_by_quote(self, search_text_quote: str) -> list[Book]:
        # TO-DO : spostare su opensearch
        list_books = self.repository.find_book_by_quote(search_text_quote)
        return list_books

    def update_book_by_Id(self, book_id: str, update_book: UpdateBook) -> BookDto:
        try:
            book = self.repository.find_by_Id(book_id)
        except Exception as e:
            raise RuntimeError(f"Request failed: update_book_by_Id find_by_Id({book_id}) -> {type(e).__name__}: {e}")

        if book is None:
            raise HTTPException(status_code=404, detail="ID non trovato!")  # coerente con get [web:84]

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

    def delete_book_by_Id(self, book_id: ObjectId):
        try:
            book_deleted = self.repository.delete(book_id)
        except Exception as e:
            raise RuntimeError(f"Request failed: delete_book_by_Id({book_id}) -> {type(e).__name__}: {e}")

        if book_deleted is None:
            return Response(status_code=404)

        return Response(status_code=200)
