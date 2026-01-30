from uuid import UUID
from fastapi import APIRouter, Depends
from pkg.dependence import Dependency
from pkg.model.reservation import Reservation, ReservationCreated, ReservationUpdate
from pkg.service.reservation_service import ReservationService


router = APIRouter(prefix='/api/internal/reservations',tags=['Reservations'])


@router.post('/v1')
def create_reservation(reservetion: ReservationCreated,service: ReservationService = Depends(Dependency.get_reservation_service)) -> Reservation:
    
     return service.create_reservation(
        book_id=reservetion.book_id,
        user_id=reservetion.user_id,
        start_reservation=reservetion.start_reservation,
        end_reservation=reservetion.end_reservation,
    )


@router.get('/{id}/v1',)
def get_reservation_by_id(id: str,service: ReservationService = Depends(Dependency.get_reservation_service)) -> Reservation:
    
    return service.get_reservation_by_Id(UUID(id))


@router.patch('/{reservation_id}/v1')
def update_reservation(
    reservation_id: UUID,
    update_reserv: ReservationUpdate,
    service: ReservationService = Depends(Dependency.get_reservation_service)) -> dict:
    
    message = service.update_reservation(update_reserv, reservation_id)
    return {"message": message}


@router.delete('/{id}/v1',)
def delete_reservation(reservation_id: str,service: ReservationService = Depends(Dependency.get_reservation_service)) -> dict:
    
    message = service.delete_reservation_by_id(UUID(reservation_id))
    return {"message": message}
    
