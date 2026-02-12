import logging
from fastapi import HTTPException, Response
from pkg.dto.reservation_dto import InsertReservation, ReservationDto
from pkg.factoty.reservation_factory import model_to_dto, insert_to_model
from pkg.repository.book_repo import BookRepository
from pkg.repository.reservation_repo import ReservationRepository
from pkg.utils.validators import validate_object_id


class ReservationService:

    def __init__(self, repository: ReservationRepository, book_repo: BookRepository):
        self.repository = repository
        self.book_repo = book_repo

    def create_reservation(self, reservation: InsertReservation) -> ReservationDto:
        logging.info(f"Creating new reservation for book_id: {reservation.book_id}")
        
        if reservation.start_reservation >= reservation.end_reservation:
            logging.warning(f"Invalid date range: start_reservation >= end_reservation")
            raise HTTPException(
                status_code=400,
                detail="The start date must be before the end!"
            )
            
        
        book_objectid =  validate_object_id(reservation.book_id, "Reservation: Book ID")
        book = self.book_repo.find_by_Id(book_objectid)

        if book is None:
            logging.warning(f"Book not found with ID: {reservation.book_id}")
            raise HTTPException(status_code=404, detail="ID book not found!")
        
        new_reservation = insert_to_model(reservation)
        result = self.repository.create(new_reservation)

        if result is None:
            logging.error("Repository returned None for create_reservation")
            raise ValueError("Reservation creation failed")

        logging.info(f"Reservation created with ID: {result._id}")
        return model_to_dto(result)


    def get_reservation_by_Id(self, reserve_id: str) -> ReservationDto:
        logging.info(f"Searching reservation by ID: {reserve_id}")
        
        reservation_objectid = validate_object_id(reserve_id, "Reservation ID")
        reservation = self.repository.find_by_Id(reservation_objectid)

        if reservation is None:
            logging.warning(f"Reservation not found with ID: {reserve_id}")
            raise HTTPException(status_code=404, detail="ID reservation not found!")

        logging.info(f"Reservation found: ID={reserve_id}")
        return model_to_dto(reservation)


    def update_reservation(self, reserve_id: str):
        logging.info(f"Updating reservation with ID: {reserve_id}")
        
        reservation_objectid = validate_object_id(reserve_id, "Reservation ID")
        reservation = self.repository.update(reservation_objectid)

        if reservation is not True:
            logging.warning(f"Reservation to update not found: {reserve_id}")
            return Response(status_code=404)

        logging.info(f"Reservation updated successfully: ID={reserve_id}")
        return Response(status_code=200)


    def delete_reservation_by_id(self, reserve_id: str):
        logging.info(f"Deleting reservation with ID: {reserve_id}")
        
        reservation_objectid = validate_object_id(reserve_id, "Reservation ID")
        deleted_reservation = self.repository.delete(reservation_objectid)

        if deleted_reservation is not True:
            logging.warning(f"Deletion failed for ID: {reserve_id}")
            return Response(status_code=400)

        logging.info(f"Reservation deleted successfully: ID={reserve_id}")
        return Response(status_code=200)