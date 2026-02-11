from fastapi import APIRouter, Depends, status
from loguru import logger
from pkg.config.mogodb import get_mongoDb
from pkg.dto.reservation_dto import InsertReservation, ReservationDto
from pkg.repository.book_repo import BookRepository
from pkg.repository.reservation_repo import ReservationRepository
from pkg.service.reservation_service import ReservationService


router = APIRouter(prefix='/api/internal/reservations',tags=['Reservations'])


mongo_db = get_mongoDb()
repo = ReservationRepository(mongo_db)
book_repo = BookRepository(mongo_db)
def get_reservation_service() -> ReservationService:
    return ReservationService(repository = repo, book_repo = book_repo)


@router.post('/v1', response_model=ReservationDto, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: InsertReservation, service: ReservationService = Depends(get_reservation_service)):
    result = service.create_reservation(reservation)
    return result


@router.get('/{id}/v1', response_model=ReservationDto)
def get_reservation_by_id(id: str, service: ReservationService = Depends(get_reservation_service)):
    result = service.get_reservation_by_Id(id)
    return result


@router.patch('/{reservation_id}/v1')
def update_reservation(reservation_id: str, service: ReservationService = Depends(get_reservation_service)):
    result = service.update_reservation(reservation_id)
    return result


@router.delete('/{id}/v1')
def delete_reservation(id: str, service: ReservationService = Depends(get_reservation_service)):
    result = service.delete_reservation_by_id(id)
    return result