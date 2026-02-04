from bson import ObjectId
from pkg.dto.reservation_dto import ReservationDto
from pkg.model.reservation import Reservation


def model_to_dto(reservation: Reservation) -> ReservationDto:
    return ReservationDto(
        id= str(reservation._id),
        book_id= str(reservation.book_id),
        user_id= str(reservation.user_id),
        start_reservation= reservation.start_reservation,
        end_reservation= reservation.end_reservation,
    )
    

def dto_to_model(reservation: ReservationDto) -> Reservation:
    return Reservation(
        _id = ObjectId(reservation.id),
        book_id= ObjectId(reservation.book_id),
        user_id = ObjectId(reservation.user_id),
        start_reservation= reservation.start_reservation,
        end_reservation= reservation.end_reservation,
    )