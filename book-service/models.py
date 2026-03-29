from pydantic import BaseModel
from typing import Optional


class BookCreate(BaseModel):
    book_id: str
    title: str
    authorId: int
    authorName: str
    genreCategory: str
    publishedYear: int
    copiesAvailable: int = 1


class BookUpdate(BaseModel):
    title: Optional[str] = None
    authorId: Optional[int] = None
    authorName: Optional[str] = None
    genreCategory: Optional[str] = None
    publishedYear: Optional[int] = None
    copiesAvailable: Optional[int] = None


class BookResponse(BaseModel):
    model_config = {"populate_by_name": True}

    id: str
    book_id: str
    title: str
    authorId: int
    authorName: str
    genreCategory: str
    publishedYear: int
    copiesAvailable: int