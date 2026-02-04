from dataclasses import dataclass, field
from bson import ObjectId
from datetime import datetime

    
@dataclass
class Reservation:
    book_id: str  
    user_id: str  
    start_reservation: datetime
    end_reservation: datetime
    _id: ObjectId = field(default_factory=ObjectId)
    
    
    @property
    def start_it(self) -> str:
        return self.start_reservation.strftime("%d/%m/%Y %H:%M")