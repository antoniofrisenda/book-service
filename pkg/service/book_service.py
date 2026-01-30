from fastapi import HTTPException
from pkg.model.book import Book, BookCreated
from pkg.repository.book_repo import BookRepository


class BookService:
    
    def __init__(self, repository: BookRepository):
        self.repository = repository
        
    def create_book(self, book: BookCreated) -> Book:
                
        if not book.title or not book.title.strip():

            raise ValueError("Il titolo è obbligatorio")
        
        if not book.genre or not book.genre.strip():
            raise ValueError("Il genere è obbligatorio")
        
        if not book.author or not book.author.strip():
            # 
            raise ValueError("L'autore è obbligatorio")
        
        
        existing = self.repository.find_by_Isbn(book.isbn)
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"Libro con ISBN {book.isbn} già esistente"
            )
            
        book_created = self.repository.create(book)
        return book_created
    
    def get_book_by_Id(self, book_id: str) -> Book:
        finded_book = self.repository.find_by_Id(book_id)
        
        return finded_book
    
    def get_book_by_author(self, author: str) -> list[Book]:
        
        finded_books = self.repository.find_by_author(author)
        
        return finded_books
    
    def get_book_by_genre(self, genre: str) -> list[Book]:
        list_finded_book = self.repository.find_by_genre(genre)
        
        return list_finded_book
    
    def get_book_by_isbn(self, isbn:str) -> Book:
        book_result = self.repository.find_by_Isbn(isbn)
        
        if book_result is None:
            raise HTTPException(status_code = 404, detail = "ISBN non trovato!")
        
        return book_result
    
    def get_books_by_quote(self, search_text_quote: str) -> list[Book]:
        
        list_books = self.repository.find_book_by_quote(search_text_quote)
        return list_books
    
    def update_book_by_Id(self, book_id: str, update_book : BookCreated) -> str:
            
            book_updated = self.repository.update(book_id, update_book)
            
            if book_updated is not None:
                return "Libro modificato con successo!"
            else:
                raise HTTPException(status_code=400, detail="Non è stato possibile modificare il libro")
        
    def delete_book_by_Id(self, book_id: str) -> str:
        
        book_deleted = self.repository.delete(book_id)
        
        if book_deleted is True:
            return "Libro eliminato con successo!"
        
        else:
            raise HTTPException(status_code=400, detail="Non è stato posibile eliminare il libro")
