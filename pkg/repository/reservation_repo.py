from typing import Optional
from uuid import UUID
from pymongo import MongoClient
from fastapi import HTTPException
from pkg.model.reservation import Reservation, ReservationCreated, ReservationUpdate


class ReservationRepository:
    
    def __init__(self, string_connection: str, db_name: str):
        self.client = MongoClient(string_connection, uuidRepresentation='standard')
        self.db = self.client[db_name]
        self.collection = self.db['reservations']
        
        self.collection.create_index([("book_id", 1), ("start_reservation", 1), ("end_reservation", 1)])
        
    def find_by_Id(self, reservation_id: UUID) -> Optional[Reservation]:
        result = self.collection.find_one({'_id': reservation_id})
        
        if result is None:
            raise HTTPException(status_code =404, detail= "Prenotazione non trovata!")
        
        return Reservation.from_mongo(result)
    
    def create(self, reservation: ReservationCreated, reservation_id: UUID) -> UUID:
       
         with self.client.start_session() as session:
            with session.start_transaction():

                
                
                conflict = self.collection.find_one({
                    "book_id": reservation.book_id,
                    "state": {"$in": ["active"]}, 
                    "start_reservation": {"$lt": reservation.end_reservation},
                    "end_reservation": {"$gt": reservation.start_reservation}
                }, session=session)
                
                if conflict:
                    raise HTTPException(
                        status_code=409,
                        detail=f"Prenotazione non disponibile dal {conflict['start_reservation']} al {conflict['end_reservation']}"
                    )
                
                
                if not reservation.state:
                    reservation.state = "active"
                    
                    
                document = reservation.model_dump()
                document['_id'] = reservation_id 
                
                
                result = self.collection.insert_one(document, session=session)
                
                
                
                return reservation_id
            
    
    def update(self, update_reserv: Reservation, reserve_id: UUID) -> bool:
        self.find_by_Id(reserve_id)
        
        result = self.collection.update_one(
            {'_id': reserve_id},
            {'$set': {
                'start_reservation': update_reserv.start_reservation,
                'end_reservation': update_reserv.end_reservation,
            }}
        )

        return result.modified_count > 0
    
    
    
    def delete(self, reserve_id: UUID) -> bool:
        result = self.collection.find_one_and_delete({'_id': reserve_id})
        
        if result is None:
            raise HTTPException(status_code=404, detail="Prenotazione non trovata!")
        
        return True

