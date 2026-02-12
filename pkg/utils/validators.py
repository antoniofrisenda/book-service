from bson import ObjectId
from fastapi import HTTPException
import logging


def validate_object_id(id: str, field_name: str = "ID") -> ObjectId:
        try:
            return ObjectId(id)
        except Exception:
            logging.warning(f"Invalid ObjectId format for {field_name}: {id}")
            raise HTTPException(status_code=400, detail=f"Invalid {field_name} format!")