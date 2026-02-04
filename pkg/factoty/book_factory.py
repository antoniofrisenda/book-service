from bson import ObjectId
from pkg.dto.book_dto import BookDto, UpdateBook
from pkg.model.book import Book


def model_to_dto(book: Book) -> BookDto:
    return BookDto(
        id= str(book._id),
        title= book.title,
        genre= book.genre,
        author= book.author,
        isbn= book.isbn,
        quotes= book.quotes
    )
    
    
def dto_to_model(book: BookDto ) -> Book:
    return Book(
       _id = ObjectId(book.id),
       title= book.title,
       genre= book.genre,
       author= book.genre,
       isbn= book.isbn,
       quotes= book.quotes
    )


def update_to_model(book_id: str, update: UpdateBook):
    return Book(
        _id=ObjectId(book_id),
        title=update.title,
        genre=update.genre,
        author=update.author,
        isbn=update.isbn,
        quotes=update.quotes
    )
