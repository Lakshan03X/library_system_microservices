from fastapi import APIRouter, HTTPException
from typing import List
from uuid import uuid4
from db import book_collection, memory_books, DB_MODE
from models import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


def using_mongo() -> bool:
    return DB_MODE == "mongo" and book_collection is not None


def book_helper(book: dict) -> dict:
    """Convert MongoDB document to response format with field mapping."""
    # Handle both _id formats (ObjectId or string)
    book_id_field = str(book.get("_id", ""))
    
    return {
        "id": book_id_field,
        "book_id": book.get("book_id", ""),
        "title": book.get("title", ""),
        "authorId": book.get("authorId", book.get("author_id", book.get("AuthorId", 0))),
        "authorName": book.get("authorName", book.get("author_name", book.get("AuthorName", ""))),
        "genreCategory": book.get("genreCategory", book.get("genre_category", book.get("GenreCategory", book.get("genre", "")))),
        "publishedYear": book.get("publishedYear", book.get("published_year", book.get("PublishedYear", book.get("year", 0)))),
        "copiesAvailable": book.get("copiesAvailable", book.get("copies_available", book.get("CopiesAvailable", book.get("copies", 0)))),
    }


@router.get("/", response_model=List[BookResponse])
def get_all_books():
    if using_mongo():
        books = list(book_collection.find())
        print(f"[Book Service] Found {len(books)} books in MongoDB")
        if books:
            print(f"[Book Service] Sample document keys: {list(books[0].keys())}")
        return [book_helper(b) for b in books]
    return [book_helper(b) for b in memory_books.values()]


@router.get("/debug")
def debug_books():
    """Debug endpoint to see raw MongoDB documents."""
    if using_mongo():
        books = list(book_collection.find())
        # Convert ObjectId to string for JSON serialization
        for book in books:
            book["_id"] = str(book["_id"])
        return {
            "db_mode": DB_MODE,
            "count": len(books),
            "raw_documents": books
        }
    return {
        "db_mode": DB_MODE,
        "count": len(memory_books),
        "raw_documents": list(memory_books.values())
    }


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: str):
    if using_mongo():
        book = book_collection.find_one({"book_id": book_id})
    else:
        book = next((b for b in memory_books.values() if b["book_id"] == book_id), None)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_helper(book)


@router.post("/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate):
    if using_mongo():
        existing = book_collection.find_one({"book_id": book.book_id})
    else:
        existing = next((b for b in memory_books.values() if b["book_id"] == book.book_id), None)

    if existing:
        raise HTTPException(status_code=400, detail="Book ID already exists")

    book_dict = book.model_dump()
    internal_id = str(uuid4())
    book_dict["_id"] = internal_id

    if using_mongo():
        book_collection.insert_one(book_dict)
    else:
        memory_books[internal_id] = book_dict

    return book_helper(book_dict)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: str, book: BookUpdate):
    if using_mongo():
        existing = book_collection.find_one({"book_id": book_id})
    else:
        existing = next((b for b in memory_books.values() if b["book_id"] == book_id), None)

    if not existing:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = {k: v for k, v in book.model_dump().items() if v is not None}

    if using_mongo():
        if update_data:
            book_collection.update_one({"book_id": book_id}, {"$set": update_data})
        updated = book_collection.find_one({"book_id": book_id})
        return book_helper(updated)

    existing.update(update_data)
    memory_books[existing["_id"]] = existing
    return book_helper(existing)


@router.delete("/{book_id}")
def delete_book(book_id: str):
    if using_mongo():
        result = book_collection.delete_one({"book_id": book_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": "Book deleted successfully"}

    existing = next((b for b in memory_books.values() if b["book_id"] == book_id), None)
    if not existing:
        raise HTTPException(status_code=404, detail="Book not found")

    del memory_books[existing["_id"]]
    return {"message": "Book deleted successfully"}