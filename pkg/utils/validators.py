from bson import ObjectId
from fastapi import HTTPException
import logging
from isbnlib import is_isbn13, mask, clean



def validate_object_id(id: str, field_name: str = "ID") -> ObjectId:
        try:
            return ObjectId(id)
        except Exception:
            logging.warning(f"Invalid ObjectId format for {field_name}: {id}")
            raise HTTPException(status_code=400, detail=f"Invalid {field_name} format!")
    
        
def validate_and_format_isbn(isbn: str) -> str:
    cleaned = clean(isbn)
    if not is_isbn13(cleaned):
        logging.warning(f"Invalid ISBN: {isbn} (cleaned: {cleaned})")
        raise HTTPException(status_code=400, detail="Invalid ISBN!")
    return mask(cleaned, "-")