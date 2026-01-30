import os
from fastapi import Depends
from pkg.repository.book_repo import BookRepository
from pkg.repository.reservation_repo import ReservationRepository
from pkg.service.book_service import BookService
from pkg.service.reservation_service import ReservationService



def get_connection_string() -> str:
        
        return os.getenv('MONGO_URL')  


def get_db_name() -> str:
        
        return os.getenv('MONGO_DB_NAME')


def get_book_repository() -> BookRepository:
        
        return BookRepository(
            string_connection=get_connection_string(),
            db_name=get_db_name()
        )


def get_reservation_repository() -> ReservationRepository:
        
        return ReservationRepository(
            string_connection=get_connection_string(),
            db_name=get_db_name()
        )


def get_book_service(
        repository: BookRepository = Depends(get_book_repository)) -> BookService:
        
        return BookService(repository)


def get_reservation_service(
        reservation_repo: ReservationRepository = Depends(get_reservation_repository),
        book_repo: BookRepository = Depends(get_book_repository)) -> ReservationService:
        
        return ReservationService(reservation_repo, book_repo)

    