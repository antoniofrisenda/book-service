from dataclasses import asdict
import logging
from bson import ObjectId
from pymongo import ASCENDING
from pkg.config.mogodb import MongoConnection
from pkg.model.author import Author


class AuthorRepository:
    def __init__(self, mongo_connection: MongoConnection):
        self.collection = mongo_connection.database.authors
        self.collection.create_index([("name", ASCENDING)], name="author_name_idx")

    def create(self, author: Author) -> Author:
        try:
            result = self.collection.insert_one(asdict(author))
            author._id = result.inserted_id
            return author
        except Exception as e:
            logging.error(f"Error with author creation: {e}")
            logging.exception("Full detail of error:")
            raise

    def find_by_id(self, author_id: ObjectId) -> Author | None:
        try:
            result = self.collection.find_one({"_id": author_id})
            if result is None:
                return None
            return Author(**result)
        except Exception as e:
            logging.error(f"Error with author search by ID {author_id}: {e}")
            logging.exception("Full detail of error:")
            raise
