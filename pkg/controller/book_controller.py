from fastapi import APIRouter, Depends, HTTPException, status
from pkg.config.mogodb import get_mongoDb
from pkg.dto.book_dto import BookDto, InsertBook, UpdateBook
from pkg.repository.book_repo import BookRepository
from pkg.service.book_service import BookService


router = APIRouter(prefix= '/api/internal/books', tags=['Books'])

mongo_db = get_mongoDb()
repo = BookRepository(mongo_db)
def get_book_service() -> BookService:
    return BookService(repo)

@router.post('/v1', response_model=BookDto, status_code= status.HTTP_201_CREATED)
def create_book(book: InsertBook, service: BookService = Depends(get_book_service)):
    
    return service.create_book(book)


@router.get('/author/v1', tags=["TO-DO"], summary="Find books by author")
def get_by_author(author : str, service: BookService = Depends(get_book_service)):
    raise HTTPException(status_code=501, detail="Not implemented yet")
    

@router.get('/genre/v1', tags=["TO-DO"], summary="Find book by genre")
def get_by_genre(genre: str,  service: BookService = Depends(get_book_service)):
    raise HTTPException(status_code=501, detail="Not implemented yet")
    


@router.get('/quote/v1', tags=["TO-DO"], summary="Find book by quotes")
def get_quotes(text_serch: str,service: BookService = Depends(get_book_service)):
    raise HTTPException(status_code=501, detail="Not implemented yet") 
 

   
@router.get('/isbn/v1', response_model=BookDto)
def get_by_isbn(isbn: str, service: BookService = Depends(get_book_service)):
    
    return service.get_book_by_isbn(isbn)


@router.get('/{book_id}/v1',response_model=BookDto)
def get_by_Id(book_id: str, service: BookService = Depends(get_book_service)):
    
    return service.get_book_by_Id(book_id)


@router.patch('/{update_id}/v1', response_model=BookDto)
def update_book(update_id: str, book: UpdateBook, service: BookService = Depends(get_book_service)):
    
    return service.update_book_by_Id(update_id, book)


@router.delete('/{id}/v1')
def delete_book(id:str, service: BookService = Depends(get_book_service)):
    
    return service.delete_book_by_Id(id)
