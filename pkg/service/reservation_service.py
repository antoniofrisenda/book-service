from datetime import datetime
from uuid import UUID, uuid4
from fastapi import HTTPException
from pkg.model.reservation import Reservation, ReservationCreated, ReservationUpdate
from pkg.repository.book_repo import BookRepository
from pkg.repository.reservation_repo import ReservationRepository


class ReservationService:
    
    def __init__(self, repository: ReservationRepository, book_repo= BookRepository):
        self.repository = repository
        self.book_repo = book_repo
        
    def create_reservation(self, book_id: str, user_id: str, start_reservation: datetime, end_reservation: datetime, state: str = "active") -> Reservation:
        
        if start_reservation >= end_reservation:
            raise HTTPException(
                status_code=400,
                detail="La data di inizio deve essere precedente alla fine"
            )
        
        if start_reservation < datetime.now():
            raise HTTPException(
                status_code=400,
                detail="Non puoi prenotare nel passato"
            )
        
        try:
            self.book_repo.find_by_Id(book_id)
        except HTTPException:
            raise HTTPException(status_code=404, detail="Libro non trovato")
        
        reservation_id = uuid4()
        
        reservation = ReservationCreated(
            book_id=book_id,
            user_id=user_id,
            start_reservation=start_reservation,
            end_reservation=end_reservation,
            state=state
        )
        
        reservation_id = self.repository.create(reservation, reservation_id)
        return self.repository.find_by_Id(reservation_id)
            
    
    def get_reservation_by_Id(self, reserve_id: UUID) -> Reservation:
        
        reservation_founded = self.repository.find_by_Id(reserve_id)
        
        return reservation_founded
    
    
    
    def update_reservation(self, update_reserv: Reservation, reserve_id: UUID) -> str:
        
        update_reservation = self.repository.update(update_reserv, reserve_id)
        
        if update_reservation is True:
            return "Prenotazione aggiornata con successo!"
        else:
            raise HTTPException(status_code=400, detail="Non è stato possibile modificare la prenotzione!") 
        
        
    def delete_reservation_by_id(self, reserv_id: UUID) -> str:
        
        deleted_reservation = self.repository.delete(reserv_id)
        
        if deleted_reservation is True:
            return "Prenotazione eliminata con successo!"
        else:
            raise HTTPException(status_code=400, detail="Non è stato possibile eliminare la prenotazione")