import logging
from fastapi import HTTPException
from pkg.dto.author_dto import AuthorDto, InsertAuthor
from pkg.factoty.author_factory import insert_to_model, model_to_dto
from pkg.repository.author_repo import AuthorRepository
from pkg.utils.validators import validate_object_id


class AuthorService:
    def __init__(self, repository: AuthorRepository):
        self.repository = repository

    def create_author(self, insert_author: InsertAuthor) -> AuthorDto:
        logging.info(f"Creating author: {insert_author.name}")

        if not insert_author.name.strip():
            raise HTTPException(status_code=400, detail="Author name is required!")

        if not insert_author.biography.strip():
            raise HTTPException(status_code=400, detail="Author biography is required!")

        created = self.repository.create(insert_to_model(insert_author))
        return model_to_dto(created)

    def get_author_by_id(self, author_id: str) -> AuthorDto:
        logging.info(f"Searching author by ID: {author_id}")

        author_object_id = validate_object_id(author_id, "Author ID")
        author = self.repository.find_by_id(author_object_id)

        if author is None:
            logging.warning(f"Author not found with ID: {author_id}")
            raise HTTPException(status_code=404, detail="Author ID not found!")

        return model_to_dto(author)
