from fastapi import APIRouter, Depends, status
from pkg.config.mogodb import get_mongoDb
from pkg.dto.author_dto import AuthorDto, InsertAuthor
from pkg.repository.author_repo import AuthorRepository
from pkg.service.author_service import AuthorService
from pkg.utils.env_validator import get_env


router = APIRouter(prefix="/api/internal/authors", tags=["Authors"])

mongo_db = get_mongoDb(mongo_url=get_env("MONGO_URI"), db_name=get_env("MONGO_DB_NAME"))
repo = AuthorRepository(mongo_db)


def get_author_service() -> AuthorService:
    return AuthorService(repo)


@router.post("/v1", response_model=AuthorDto, status_code=status.HTTP_201_CREATED)
def create_author(author: InsertAuthor, service: AuthorService = Depends(get_author_service)):
    return service.create_author(author)


@router.get("/{author_id}/v1", response_model=AuthorDto)
def get_author_by_id(author_id: str, service: AuthorService = Depends(get_author_service)):
    return service.get_author_by_id(author_id)
