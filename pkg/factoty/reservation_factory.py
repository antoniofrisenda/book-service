from pkg.dto.reservation_dto import InsertReservation, ReservationDto
from pkg.model.reservation import Reservation


def model_to_dto(reservation: Reservation) -> ReservationDto:
    return ReservationDto(
        id= str(reservation._id),
        book_id= str(reservation.book_id),
        user_id= str(reservation.user_id),
        start_reservation= reservation.start_reservation,
        end_reservation= reservation.end_reservation,
    )
    

def insert_to_model(insert: InsertReservation) -> Reservation:
    return Reservation(
        book_id= insert.book_id,
        user_id = insert.user_id,
        start_reservation= insert.start_reservation,
        end_reservation= insert.end_reservation,
    )