from fastapi import APIRouter, Depends
from pkg.dependence import Dependency
from pkg.model.book import Book, BookCreated
from pkg.service.book_service import BookService


router = APIRouter(prefix= '/api/internal/books', tags=['Books'])


@router.post('/v1')
def create_book(book: BookCreated, service: BookService = Depends(Dependency.get_book_service)):
    
    return service.create_book(book)


@router.get('/author/v1')
def get_by_author(author : str, service: BookService = Depends(Dependency.get_book_service)) -> list[Book]:
    
    return service.get_book_by_author(author)

@router.get('/genre/v1')
def get_by_genre(genre: str,  service: BookService = Depends(Dependency.get_book_service)) -> list[Book]:
    
    return service.get_book_by_genre(genre) 


@router.get('/quote/v1')
def get_quotes(text_serch: str,service: BookService = Depends(Dependency.get_book_service)) -> list[Book]:
    
    return service.get_books_by_quote(text_serch)


@router.get('/{id}/v1')
def get_by_Id(id: str, service: BookService = Depends(Dependency.get_book_service)) -> Book:
    
    return service.get_book_by_Id(id)

@router.patch('/v1')
def update_book(id: str, book: BookCreated, service: BookService = Depends(Dependency.get_book_service)) -> str:
    
    return service.update_book_by_Id(id, book)


@router.delete('/v1')
def delete_book(id:str, service: BookService = Depends(Dependency.get_book_service)) -> str:
    
    return service.delete_book_by_Id(id)


