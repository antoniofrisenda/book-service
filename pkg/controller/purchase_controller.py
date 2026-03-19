from fastapi import APIRouter, Depends, status
from pkg.config.mogodb import get_mongoDb
from pkg.dto.purchase_dto import InsertPurchase, PurchaseDto
from pkg.repository.book_repo import BookRepository
from pkg.repository.purchase_repo import PurchaseRepository
from pkg.service.purchase_service import PurchaseService
from pkg.utils.env_validator import get_env


router = APIRouter(prefix='/api/internal/purchases', tags=['Purchases'])

mongo_db = get_mongoDb(mongo_url=get_env("MONGO_URI"), db_name=get_env("MONGO_DB_NAME"))
repo = PurchaseRepository(mongo_db)
book_repo = BookRepository(mongo_db)


def get_purchase_service() -> PurchaseService:
    return PurchaseService(repository=repo, book_repo=book_repo)


@router.post('/v1', response_model=PurchaseDto, status_code=status.HTTP_201_CREATED)
def buy_book(purchase: InsertPurchase, service: PurchaseService = Depends(get_purchase_service)):
    result = service.buy_book(purchase)
    return result


@router.get('/user/{user_id}/v1', response_model=list[PurchaseDto])
def get_purchases_by_user(user_id: str, service: PurchaseService = Depends(get_purchase_service)):
    result = service.get_purchases_by_user(user_id)
    return result
