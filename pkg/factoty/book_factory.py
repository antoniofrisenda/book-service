from bson import ObjectId
from pkg.dto.book_dto import BookDto, InsertBook, UpdateBook
from pkg.model.book import Book


def model_to_dto(book: Book) -> BookDto:
    return BookDto(
        id= str(book._id),
        title= book.title,
        genre= book.genre,
        author= book.author,
        isbn= book.isbn,
        price= book.price,
        quotes= book.quotes
    )


def update_to_model(book_id: str, update: UpdateBook):
    return Book(
        _id=ObjectId(book_id),
        title=update.title,
        genre=update.genre,
        author=update.author,
        isbn=update.isbn,
        price=update.price,
        quotes=update.quotes
    )
    
    
def insert_to_model(insert: InsertBook):
    return Book(
        title=insert.title,
        genre=insert.genre,
        author=insert.author,
        isbn=insert.isbn,
        price=insert.price,
        quotes=insert.quotes
    )
