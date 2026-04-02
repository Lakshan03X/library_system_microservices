from datetime import datetime
from enum import Enum
import os
from typing import List, Optional
from pydantic import BaseModel, Field
import requests
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Service URLs from .env
BOOK_SERVICE = os.getenv("BOOK_SERVICE")
MEMBER_SERVICE = os.getenv("MEMBER_SERVICE")
BORROW_SERVICE = os.getenv("BORROW_SERVICE")
REVIEW_SERVICE = os.getenv("REVIEW_SERVICE")
STAFF_SERVICE = os.getenv("STAFF_SERVICE")
RESERVATION_SERVICE = os.getenv("RESERVATION_SERVICE")


def _safe_forward(method: str, url: str, payload: dict | None = None):
    try:
        resp = requests.request(method=method, url=url, json=payload, timeout=10)
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Upstream service unavailable: {exc}")

    content_type = (resp.headers.get("content-type") or "").lower()
    if "application/json" in content_type:
        body = resp.json()
    else:
        body = {"detail": resp.text or "Upstream service returned non-JSON response"}

    if resp.status_code >= 400:
        detail = body.get("detail") if isinstance(body, dict) else body
        raise HTTPException(status_code=resp.status_code, detail=detail)

    return body


# ===============================================================
# BOOK MODELS
# ===============================================================
# --------------- BOOK SERVICE ROUTES ---------------
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


# --------------- BOOK SERVICE ROUTES ---------------
@router.get("/books")
def get_books():
    return _safe_forward("GET", f"{BOOK_SERVICE}/books")

@router.get("/books/{book_id}")
def get_book(book_id: str):
    return _safe_forward("GET", f"{BOOK_SERVICE}/books/{book_id}")

@router.post("/books", status_code=201)
def create_book(payload: BookCreate):
    return _safe_forward("POST", f"{BOOK_SERVICE}/books", payload.model_dump(mode="json"))

@router.put("/books/{book_id}")
def update_book(book_id: str, payload: BookUpdate):
    return _safe_forward("PUT", f"{BOOK_SERVICE}/books/{book_id}", payload.model_dump(mode="json", exclude_unset=True))

@router.delete("/books/{book_id}")
def delete_book(book_id: str):
    return _safe_forward("DELETE", f"{BOOK_SERVICE}/books/{book_id}")

# ===============================================================
# MEMBER MODELS
# ===============================================================
class MemberCreate(BaseModel):
    member_id: str
    full_name: str
    email: str
    phone: str
    address: str
    membership_type: str
    national_id: str
    status: str = "active"

    class Config:
        json_schema_extra = {
            "example": {
                "member_id": "MEM001",
                "full_name": "Kasun Perera",
                "email": "kasun@gmail.com",
                "phone": "0771234567",
                "address": "No 12, Galle Road, Colombo 03",
                "membership_type": "student",
                "national_id": "200012345678"
            }
        }


class MemberUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    membership_type: Optional[str] = None
    national_id: Optional[str] = None
    status: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                
                "email": "kasun@gmail.com",
                "phone": "0771234567",
                "address": "No 12, Galle Road, Colombo 03",
                
            }
        }


# --------------- MEMBER SERVICE ROUTES ---------------
@router.get("/members")
def get_members():
    return _safe_forward("GET", f"{MEMBER_SERVICE}/members/")

@router.get("/members/{member_id}")
def get_member(member_id: str):
    return _safe_forward("GET", f"{MEMBER_SERVICE}/members/{member_id}")

@router.post("/members", status_code=201)
def create_member(payload: MemberCreate):
    return _safe_forward("POST", f"{MEMBER_SERVICE}/members/", payload.model_dump())

@router.put("/members/{member_id}")
def update_member(member_id: str, payload: MemberUpdate):
    return _safe_forward("PUT", f"{MEMBER_SERVICE}/members/{member_id}", payload.model_dump(exclude_unset=True))

@router.delete("/members/{member_id}")
def delete_member(member_id: str):
    return _safe_forward("DELETE", f"{MEMBER_SERVICE}/members/{member_id}")


# ===============================================================
# STAFF MODELS
# ===============================================================
class StaffCreate(BaseModel):
    staff_id: str
    name: str
    email: str
    role: str

    class Config:
        json_schema_extra = {
            "example": {
                "staff_id": "STF001",
                "name": "Nimal Silva",
                "email": "nimal@library.com",
                "role": "librarian"
            }
        }


class StaffUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Nimal Silva",
                "email": "nimal@library.com",
                "role": "librarian"
            }
        }


# --------------- STAFF SERVICE ROUTES ---------------
@router.get("/staff")
def get_staff():
    return _safe_forward("GET", f"{STAFF_SERVICE}/staffs/")

@router.get("/staff/{staff_id}")
def get_staff_by_id(staff_id: str):
    return _safe_forward("GET", f"{STAFF_SERVICE}/staffs/{staff_id}")

@router.post("/staff", status_code=201)
def create_staff(payload: StaffCreate):
    return _safe_forward("POST", f"{STAFF_SERVICE}/staffs/", payload.model_dump())

@router.put("/staff/{staff_id}")
def update_staff(staff_id: str, payload: StaffUpdate):
    return _safe_forward("PUT", f"{STAFF_SERVICE}/staffs/{staff_id}", payload.model_dump(exclude_unset=True))

@router.delete("/staff/{staff_id}")
def delete_staff(staff_id: str):
    return _safe_forward("DELETE", f"{STAFF_SERVICE}/staffs/{staff_id}")


# ===============================================================
# BORROW SERVICE ROUTES
# ===============================================================
class BorrowStatus(str, Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"
    OVERDUE = "overdue"

class BorrowCreate(BaseModel):
    borrow_id: str
    book_id: List[str]
    member_id: str
    borrow_date: datetime = Field(default_factory=datetime.utcnow)
    due_date: datetime
    status: BorrowStatus = BorrowStatus.BORROWED


class BorrowUpdate(BaseModel):
    book_id: Optional[List[str]] = None
    member_id: Optional[str] = None
    borrow_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    status: Optional[BorrowStatus] = None


# --------------- BORROW SERVICE ROUTES ---------------
@router.get("/borrows")
def get_all_borrows():
    return _safe_forward("GET", f"{BORROW_SERVICE}/borrows/")

@router.get("/borrows/status/overdue")
def get_overdue_borrows():
    return _safe_forward("GET", f"{BORROW_SERVICE}/borrows/status/overdue")

@router.get("/borrows/member/{member_id}")
def get_borrows_by_member(member_id: str):
    return _safe_forward("GET", f"{BORROW_SERVICE}/borrows/member/{member_id}")

@router.get("/borrows/book/{book_id}")
def get_borrows_by_book(book_id: str):
    return _safe_forward("GET", f"{BORROW_SERVICE}/borrows/book/{book_id}")

@router.get("/borrows/{borrow_id}")
def get_borrow(borrow_id: str):
    return _safe_forward("GET", f"{BORROW_SERVICE}/borrows/{borrow_id}")

@router.post("/borrows")
def create_borrow(payload: BorrowCreate):
    return _safe_forward("POST", f"{BORROW_SERVICE}/borrows/", payload.model_dump(mode="json"))

@router.put("/borrows/{borrow_id}")
def update_borrow(borrow_id: str, payload: BorrowUpdate):
    return _safe_forward("PUT", f"{BORROW_SERVICE}/borrows/{borrow_id}", payload.model_dump(mode="json", exclude_unset=True))

@router.delete("/borrows/{borrow_id}")
def delete_borrow(borrow_id: str):
    return _safe_forward("DELETE", f"{BORROW_SERVICE}/borrows/{borrow_id}")

@router.put("/borrows/{borrow_id}/return")
def return_book(borrow_id: str):
    return _safe_forward("PUT", f"{BORROW_SERVICE}/borrows/{borrow_id}/return")

@router.put("/borrows/{borrow_id}/overdue")
def mark_overdue(borrow_id: str):
    return _safe_forward("PUT", f"{BORROW_SERVICE}/borrows/{borrow_id}/overdue")


# ===============================================================
# REVIEW SERVICE ROUTES
# ===============================================================
class ReviewCreate(BaseModel):
    book_id: str
    member_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    review_date: datetime = Field(default_factory=datetime.utcnow)


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
    review_date: Optional[datetime] = None


class ReviewResponse(BaseModel):
    id: str
    book_id: str
    member_id: str
    rating: int
    comment: Optional[str] = None
    review_date: datetime


# --------------- REVIEW SERVICE ROUTES ---------------
@router.get("/reviews")
def get_all_reviews():
    return _safe_forward("GET", f"{REVIEW_SERVICE}/reviews/")

@router.get("/reviews/book/{book_id}")
def get_reviews_by_book(book_id: str):
    return _safe_forward("GET", f"{REVIEW_SERVICE}/reviews/book/{book_id}")

@router.get("/reviews/member/{member_id}")
def get_reviews_by_member(member_id: str):
    return _safe_forward("GET", f"{REVIEW_SERVICE}/reviews/member/{member_id}")

@router.get("/reviews/{review_id}")
def get_review(review_id: str):
    return _safe_forward("GET", f"{REVIEW_SERVICE}/reviews/{review_id}")

@router.post("/reviews")
def create_review(payload: ReviewCreate):
    return _safe_forward("POST", f"{REVIEW_SERVICE}/reviews/", payload.model_dump(mode="json"))

@router.put("/reviews/{review_id}")
def update_review(review_id: str, payload: ReviewUpdate):
    return _safe_forward("PUT", f"{REVIEW_SERVICE}/reviews/{review_id}", payload.model_dump(mode="json", exclude_unset=True))

@router.delete("/reviews/{review_id}")
def delete_review(review_id: str):
    return _safe_forward("DELETE", f"{REVIEW_SERVICE}/reviews/{review_id}")


# ===============================================================
# RESERVATION MODELS
# ===============================================================
class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class ReservationCreate(BaseModel):
    book_id: str
    member_id: str
    reserved_date: datetime = Field(default_factory=datetime.utcnow)
    expiry_date: datetime
    status: ReservationStatus = ReservationStatus.PENDING


class ReservationUpdate(BaseModel):
    book_id: Optional[str] = None
    member_id: Optional[str] = None
    reserved_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    confirmed_date: Optional[datetime] = None
    status: Optional[ReservationStatus] = None


# --------------- RESERVATION SERVICE ROUTES ---------------
@router.get("/reservations")
def get_reservations():
    return _safe_forward("GET", f"{RESERVATION_SERVICE}/reservations")

@router.get("/reservations/member/{member_id}")
def get_reservations_by_member(member_id: str):
    return _safe_forward("GET", f"{RESERVATION_SERVICE}/reservations/member/{member_id}")

@router.get("/reservations/book/{book_id}")
def get_reservations_by_book(book_id: str):
    return _safe_forward("GET", f"{RESERVATION_SERVICE}/reservations/book/{book_id}")

@router.get("/reservations/{reservation_id}")
def get_reservation(reservation_id: str):
    return _safe_forward("GET", f"{RESERVATION_SERVICE}/reservations/{reservation_id}")

@router.post("/reservations")
def create_reservation(payload: ReservationCreate):
    return _safe_forward("POST", f"{RESERVATION_SERVICE}/reservations", payload.model_dump(mode="json"))

@router.put("/reservations/{reservation_id}")
def update_reservation(reservation_id: str, payload: ReservationUpdate):
    return _safe_forward("PUT", f"{RESERVATION_SERVICE}/reservations/{reservation_id}", payload.model_dump(mode="json", exclude_unset=True))

@router.put("/reservations/{reservation_id}/confirm")
def confirm_reservation(reservation_id: str):
    return _safe_forward("PUT", f"{RESERVATION_SERVICE}/reservations/{reservation_id}/confirm")

@router.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: str):
    return _safe_forward("DELETE", f"{RESERVATION_SERVICE}/reservations/{reservation_id}")