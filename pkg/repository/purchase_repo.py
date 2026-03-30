from dataclasses import asdict
import logging
from bson import ObjectId
from pymongo import DESCENDING
from pkg.config.mogodb import MongoConnection
from pkg.model.purchase import Purchase


class PurchaseRepository:

    def __init__(self, connection: MongoConnection):
        self.collection = connection.database.purchases
        self.collection.create_index([("user_id", DESCENDING), ("created_at", DESCENDING)])

    def create(self, purchase: Purchase) -> Purchase:
        try:
            result = self.collection.insert_one(asdict(purchase))
            purchase._id = result.inserted_id
            return purchase
        except Exception as e:
            logging.error(f"Error with purchase creation: {e}")
            logging.exception("Full detail of error:")
            raise

    def find_by_id(self, purchase_id: ObjectId) -> Purchase | None:
        try:
            result = self.collection.find_one({"_id": purchase_id})
            if result is None:
                return None
            return Purchase(**result)
        except Exception as e:
            logging.error(f"Error with the research of this purchase ID: {purchase_id}: {e}")
            logging.exception("Full detail of error:")
            raise

    def find_by_user_id(self, user_id: str) -> list[Purchase]:
        try:
            results = self.collection.find({"user_id": user_id}).sort("created_at", DESCENDING)
            return [Purchase(**doc) for doc in results]
        except Exception as e:
            logging.error(f"Error finding purchases for user_id: {user_id}: {e}")
            logging.exception("Full detail of error:")
            raise
