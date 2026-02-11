from dataclasses import asdict
from loguru import logger
from datetime import datetime, timezone
from bson import ObjectId
from fastapi import HTTPException
from pkg.config.mogodb import MongoConnection
from pkg.model.reservation import Reservation


class ReservationRepository:
    
    def __init__(self, connection: MongoConnection):
        self.collection = connection.database.reservations
        self.client = connection.client
        self.collection.create_index([("book_id", 1), ("start_reservation", 1), ("end_reservation", 1)])
        
    def find_by_Id(self, reservation_id: ObjectId) -> Reservation | None:
        try:
            result = self.collection.find_one({'_id': ObjectId(reservation_id)})
            
            if result is None:
                return None
            
            return Reservation(**result)
        
        except Exception as e:
            logger.error(f"Error with the research of this reservation ID: {reservation_id}: {e}")
            logger.exception("Full detail of error:")
            raise


    def create(self, reservation: Reservation) -> Reservation:
        try:
            #with self.client.start_session() as session:
                #with session.start_transaction():
                    conflict = self.collection.find_one({
                        "book_id": reservation.book_id,
                        "start_reservation": {"$lt": reservation.end_reservation},
                        "end_reservation": {"$gt": reservation.start_reservation}
                    })
                    
                                    
                    if conflict:
                        logger.warning(f"Conflit with {conflict['start_reservation']} and {conflict['end_reservation']}")
                        raise HTTPException(
                            status_code=409,
                            detail=f"Reservation not allowed from {conflict['start_reservation']} to {conflict['end_reservation']}"
                        )
                    
                    
                    result = self.collection.insert_one(asdict(reservation))
                    
                    reservation._id = result.inserted_id
                    return reservation
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error with reservation creation: {e}")
            logger.exception("Full detail of error:")
            raise


        
    def update(self, reserve_id: ObjectId) -> bool:
        try:
            now = datetime.now(timezone.utc)

            result = self.collection.update_one(
                {"_id": ObjectId(reserve_id)},
                {"$set": {"end_reservation": now}},
            )
            
            if result.modified_count == 0:
                return False
            
            return result.modified_count > 0
        
        except Exception as e:
            logger.error(f"Error with reservation update: {e}")
            logger.exception("Full detail of error:")
            raise
        
        

        
    def delete(self, reserve_id: ObjectId) -> bool:
        try:
            result = self.collection.delete_one({'_id': ObjectId(reserve_id)})

            if result.deleted_count == 0:
                return False
            
            return result.deleted_count == 1
        
        except Exception as e:
            logger.error(f"Error deleting reservation with ID {reserve_id}: {e}")
            logger.exception("Full detail of error:")
            raise