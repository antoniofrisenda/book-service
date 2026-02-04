from datetime import datetime, timezone
from bson import ObjectId
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
        
        book = self.book_repo.find_by_Id(reservation.book_id)
        
        if book is None:
            raise HTTPException(status_code=404, detail="Id del libro non trovato")
            
        result = self.repository.create(reservation)
        
        return model_to_dto(result)
            
    
    def get_reservation_by_Id(self, reserve_id: str) -> ReservationDto:
        
        reservation = self.repository.find_by_Id(reserve_id)
        
        if reservation is None:
            raise HTTPException(status_code=404, detail="ID prenotazione non trovato")
        
        return model_to_dto(reservation)
    
    
    
    def update_reservation(self, reserve_id: str):
        
        reservation = self.repository.update(reserve_id)
        
        if reservation is not True:
            return Response(status_code=404)
        
        return Response(status_code=200)
        
        
        
    def delete_reservation_by_id(self, reserv_id: str):
        
        deleted_reservation = self.repository.delete(reserv_id)
        
        if deleted_reservation is not True:
            return Response(status_code=400)
        
        return Response(status_code=200)