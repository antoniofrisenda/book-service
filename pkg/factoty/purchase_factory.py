from datetime import datetime, timezone
from pkg.dto.purchase_dto import InsertPurchase, PurchaseDto
from pkg.model.purchase import Purchase


def model_to_dto(purchase: Purchase) -> PurchaseDto:
    return PurchaseDto(
        id=str(purchase._id),
        userId=purchase.user_id,
        bookId=purchase.book_id,
        total=purchase.total,
        createdAt=purchase.created_at,
    )


def insert_to_model(insert: InsertPurchase, total: float) -> Purchase:
    return Purchase(
        user_id=insert.userId,
        book_id=insert.bookId,
        total=round(total, 2),
        created_at=datetime.now(timezone.utc),
    )
