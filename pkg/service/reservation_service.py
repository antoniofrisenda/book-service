from fastapi import HTTPException, Response
from pkg.dto.reservation_dto import InsertReservation, ReservationDto
from pkg.factoty.reservation_factory import model_to_dto
from pkg.repository.book_repo import BookRepository
from pkg.repository.reservation_repo import ReservationRepository


class ReservationService:

    def __init__(self, repository: ReservationRepository, book_repo: BookRepository):
        self.repository = repository
        self.book_repo = book_repo

    def create_reservation(self, reservation: InsertReservation) -> ReservationDto:

        if reservation.start_reservation >= reservation.end_reservation:
            raise HTTPException(
                status_code=400,
                detail="La data di inizio deve essere precedente alla fine"
            )

        try:
            book = self.book_repo.find_by_Id(reservation.book_id)
        except Exception as e:
            raise RuntimeError(
                f"Request failed: create_reservation find_by_Id({reservation.book_id}) -> {type(e).__name__}: {e}"
            )

        if book is None:
            raise HTTPException(status_code=404, detail="Id del libro non trovato")

        try:
            result = self.repository.create(reservation)
        except Exception as e:
            raise RuntimeError(
                f"Request failed: create_reservation create(book_id={reservation.book_id}) -> {type(e).__name__}: {e}"
            )

        if result is None:
            raise RuntimeError("Something went wrong: create_reservation returned None")

        return model_to_dto(result)

    def get_reservation_by_Id(self, reserve_id: str) -> ReservationDto:

        try:
            reservation = self.repository.find_by_Id(reserve_id)
        except Exception as e:
            raise RuntimeError(
                f"Request failed: get_reservation_by_Id({reserve_id}) -> {type(e).__name__}: {e}"
            )

        if reservation is None:
            raise HTTPException(status_code=404, detail="ID prenotazione non trovato")

        return model_to_dto(reservation)

    def update_reservation(self, reserve_id: str):

        try:
            reservation = self.repository.update(reserve_id)
        except Exception as e:
            raise RuntimeError(
                f"Request failed: update_reservation({reserve_id}) -> {type(e).__name__}: {e}"
            )

        if reservation is not True:
            return Response(status_code=404)

        return Response(status_code=200)

    def delete_reservation_by_id(self, reserv_id: str):

        try:
            deleted_reservation = self.repository.delete(reserv_id)
        except Exception as e:
            raise RuntimeError(
                f"Request failed: delete_reservation_by_id({reserv_id}) -> {type(e).__name__}: {e}"
            )

        if deleted_reservation is not True:
            return Response(status_code=400)

        return Response(status_code=200)
