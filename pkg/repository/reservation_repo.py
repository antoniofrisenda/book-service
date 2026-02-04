from dataclasses import asdict
from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException
from pkg.config.mogodb import MongoConnection
from pkg.model.reservation import Reservation


class ReservationRepository:
    
    def __init__(self, connection: MongoConnection):
        self.collection = connection.database.reservations
        self.client = connection.client
        self.collection.create_index([("book_id", 1), ("start_reservation", 1), ("end_reservation", 1)])
        
    def find_by_Id(self, reservation_id: ObjectId) -> Optional[Reservation]:
        result = self.collection.find_one({'_id': ObjectId(reservation_id)})
        
        if result is None: return None
        
        return Reservation(**result)
    
    def create(self, reservation: Reservation) -> Reservation:
        
        #with self.client.start_session() as session:
            #with session.start_transaction():
                conflict = self.collection.find_one({
                    "book_id": reservation.book_id,
                    "start_reservation": {"$lt": reservation.end_reservation},
                    "end_reservation": {"$gt": reservation.start_reservation}
                })
                
                                
                if conflict:
                    raise HTTPException(
                        status_code=409,
                        detail=f"Prenotazione non disponibile dal {conflict['start_reservation']} al {conflict['end_reservation']}"
                    )
                
                
                result = self.collection.insert_one(asdict(reservation))
                
                reservation._id = result.inserted_id
                return reservation
            
    
    def update(self, reserve_id: ObjectId) -> bool:
        
        now = datetime.now(timezone.utc)

        result = self.collection.update_one(
            {"_id": ObjectId(reserve_id)},
            {"$set": {"end_reservation": now}},
        )
        
        return result.modified_count > 0
    
    
    
    def delete(self, reserve_id: ObjectId) -> bool:
        result = self.collection.delete_one({'_id': ObjectId(reserve_id)})

        return result.deleted_count == 1

