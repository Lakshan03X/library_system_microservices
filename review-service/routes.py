from fastapi import APIRouter, HTTPException
from typing import List
from uuid import uuid4
import os
import requests
from dotenv import load_dotenv
from db import review_collection, memory_reviews, DB_MODE
from models import ReviewCreate, ReviewUpdate, ReviewResponse

load_dotenv()

router = APIRouter(prefix="/reviews", tags=["Reviews"])

# Service URLs for validation
BOOK_SERVICE = os.getenv("BOOK_SERVICE", "http://localhost:8081")
MEMBER_SERVICE = os.getenv("MEMBER_SERVICE", "http://localhost:8082")


def using_mongo() -> bool:
    return DB_MODE == "mongo" and review_collection is not None


def validate_book_exists(book_id: str) -> bool:
    """Validate that a book exists in the book service."""
    try:
        resp = requests.get(f"{BOOK_SERVICE}/books/{book_id}", timeout=5)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def validate_member_exists(member_id: str) -> bool:
    """Validate that a member exists in the member service."""
    try:
        resp = requests.get(f"{MEMBER_SERVICE}/api/members/{member_id}", timeout=5)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def review_helper(review) -> dict:
    return {
        "id": str(review["_id"]),
        "book_id": review["book_id"],
        "member_id": review["member_id"],
        "rating": review["rating"],
        "comment": review.get("comment"),
        "review_date": review["review_date"],
    }


@router.get("/", response_model=List[ReviewResponse])
def get_all_reviews():
    if using_mongo():
        return [review_helper(r) for r in review_collection.find()]
    return [review_helper(r) for r in memory_reviews.values()]


@router.get("/{id}", response_model=ReviewResponse)
def get_review(id: str):
    if using_mongo():
        review = review_collection.find_one({"_id": id})
    else:
        review = memory_reviews.get(id)

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review_helper(review)


@router.get("/book/{book_id}", response_model=List[ReviewResponse])
def get_reviews_by_book(book_id: str):
    if using_mongo():
        return [review_helper(r) for r in review_collection.find({"book_id": book_id})]
    return [review_helper(r) for r in memory_reviews.values() if r["book_id"] == book_id]


@router.get("/member/{member_id}", response_model=List[ReviewResponse])
def get_reviews_by_member(member_id: str):
    if using_mongo():
        return [review_helper(r) for r in review_collection.find({"member_id": member_id})]
    return [review_helper(r) for r in memory_reviews.values() if r["member_id"] == member_id]


@router.post("/", response_model=ReviewResponse, status_code=201)
def create_review(review: ReviewCreate):
    # Validate book exists
    if not validate_book_exists(review.book_id):
        raise HTTPException(status_code=400, detail=f"Book '{review.book_id}' not found in book service")
    
    # Validate member exists
    if not validate_member_exists(review.member_id):
        raise HTTPException(status_code=400, detail=f"Member '{review.member_id}' not found in member service")
    
    review_dict = review.model_dump()
    internal_id = str(uuid4())
    review_dict["_id"] = internal_id

    if using_mongo():
        review_collection.insert_one(review_dict)
    else:
        memory_reviews[internal_id] = review_dict

    return review_helper(review_dict)


@router.put("/{id}", response_model=ReviewResponse)
def update_review(id: str, review: ReviewUpdate):
    if using_mongo():
        existing = review_collection.find_one({"_id": id})
    else:
        existing = memory_reviews.get(id)

    if not existing:
        raise HTTPException(status_code=404, detail="Review not found")

    update_data = {k: v for k, v in review.model_dump().items() if v is not None}

    if using_mongo():
        if update_data:
            review_collection.update_one({"_id": id}, {"$set": update_data})
        updated = review_collection.find_one({"_id": id})
        return review_helper(updated)

    existing.update(update_data)
    memory_reviews[id] = existing
    return review_helper(existing)


@router.delete("/{id}")
def delete_review(id: str):
    if using_mongo():
        result = review_collection.delete_one({"_id": id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Review not found")
        return {"message": "Review deleted successfully"}

    if id not in memory_reviews:
        raise HTTPException(status_code=404, detail="Review not found")
    del memory_reviews[id]
    return {"message": "Review deleted successfully"}