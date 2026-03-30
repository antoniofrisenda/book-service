from pkg.dto.author_dto import AuthorDto, InsertAuthor
from pkg.model.author import Author


def model_to_dto(author: Author) -> AuthorDto:
    return AuthorDto(
        id=str(author._id),
        name=author.name,
        birthDate=author.birth_date,
        biography=author.biography,
    )


def insert_to_model(insert: InsertAuthor) -> Author:
    return Author(
        name=insert.name,
        birth_date=insert.birthDate,
        biography=insert.biography,
    )
