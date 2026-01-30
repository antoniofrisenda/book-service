from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from uuid import UUID, uuid4


class ReservationCreated(BaseModel):
    book_id: str  
    user_id: str  
    start_reservation: datetime
    end_reservation: datetime
    state: str
    
    @field_validator('start_reservation', 'end_reservation', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, '%d/%m/%Y %H:%M:%S')
        elif isinstance(v, datetime):
            return v
        raise ValueError(f'Formato datetime non valido: {v}')
        
    @classmethod
    def from_mongo(cls, doc: dict) -> 'ReservationCreated':    
        return cls(**doc)


class ReservationUpdate(BaseModel):
    start_reservation: datetime
    end_reservation: datetime
    
    @field_validator('start_reservation','end_reservation', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, '%d/%m/%Y %H:%M:%S')
        elif isinstance(v, datetime):
            return v
        raise ValueError(f'Formato datetime non valido: {v}')
        
    @classmethod
    def from_mongo(cls, doc: dict) -> 'ReservationUpdate':    
        return cls(**doc)


class Reservation(BaseModel):
    book_id: str  
    user_id: str  
    start_reservation: datetime
    end_reservation: datetime
    state: str
    id: UUID = Field(default_factory=uuid4, alias="_id")
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={UUID: str, datetime: lambda v: v.isoformat()}
    )
    
    @field_validator('start_reservation', 'end_reservation', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, '%d/%m/%Y %H:%M:%S')
        elif isinstance(v, datetime):
            return v
        raise ValueError(f'Formato datetime non valido: {v}')
        
    @classmethod
    def from_mongo(cls, doc: dict) -> 'Reservation':
            
            return cls(**doc)