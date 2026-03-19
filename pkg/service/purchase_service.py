import logging
from fastapi import HTTPException
from pkg.dto.purchase_dto import InsertPurchase, PurchaseDto
from pkg.factoty.purchase_factory import insert_to_model, model_to_dto
from pkg.repository.book_repo import BookRepository
from pkg.repository.purchase_repo import PurchaseRepository
from pkg.utils.validators import validate_object_id


class PurchaseService:

    def __init__(self, repository: PurchaseRepository, book_repo: BookRepository):
        self.repository = repository
        self.book_repo = book_repo

    def buy_book(self, purchase: InsertPurchase) -> PurchaseDto:
        logging.info(f"Creating purchase for book_id: {purchase.bookId} and user_id: {purchase.userId}")

        if not purchase.userId.strip():
            raise HTTPException(status_code=400, detail="userId is required!")

        book_object_id = validate_object_id(purchase.bookId, "Purchase: Book ID")
        book = self.book_repo.find_by_Id(book_object_id)

        if book is None:
            logging.warning(f"Book not found with ID: {purchase.bookId}")
            raise HTTPException(status_code=404, detail="ID book not found!")

        new_purchase = insert_to_model(purchase, total=book.price)
        created = self.repository.create(new_purchase)
        return model_to_dto(created)

    def get_purchases_by_user(self, user_id: str) -> list[PurchaseDto]:
        logging.info(f"Fetching purchases for user_id: {user_id}")

        if not user_id.strip():
            raise HTTPException(status_code=400, detail="userId is required!")

        purchases = self.repository.find_by_user_id(user_id)
        return [model_to_dto(p) for p in purchases]
