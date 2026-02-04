from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReservationDto:
    id: str
    book_id: str  
    user_id: str  
    start_reservation: datetime
    end_reservation: datetime
    

@dataclass
class InsertReservation:
    book_id: str  
    user_id: str  
    start_reservation: datetime
    end_reservation: datetime
    


    