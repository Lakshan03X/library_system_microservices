from datetime import datetime
from enum import Enum
import os
from typing import Optional
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


# --------------- BOOK SERVICE ROUTES ---------------
@router.get("/books")
def get_books():
    resp = requests.get(f"{BOOK_SERVICE}/books")
    return resp.json()

@router.post("/books")
def create_book(payload: dict):
    resp = requests.post(f"{BOOK_SERVICE}/books", json=payload)
    return resp.json()

@router.put("/books/{book_id}")
def update_book(book_id: str, payload: dict):
    resp = requests.put(f"{BOOK_SERVICE}/books/{book_id}", json=payload)
    return resp.json()

@router.delete("/books/{book_id}")
def delete_book(book_id: str):
    resp = requests.delete(f"{BOOK_SERVICE}/books/{book_id}")
    return resp.json()


# --------------- MEMBER SERVICE ROUTES ---------------
@router.get("/members")
def get_members():
    resp = requests.get(f"{MEMBER_SERVICE}/members")
    return resp.json()

@router.post("/members")
def create_member(payload: dict):
    resp = requests.post(f"{MEMBER_SERVICE}/members", json=payload)
    return resp.json()

@router.put("/members/{member_id}")
def update_member(member_id: str, payload: dict):
    resp = requests.put(f"{MEMBER_SERVICE}/members/{member_id}", json=payload)
    return resp.json()

@router.delete("/members/{member_id}")
def delete_member(member_id: str):
    resp = requests.delete(f"{MEMBER_SERVICE}/members/{member_id}")
    return resp.json()


# --------------- BORROW SERVICE ROUTES ---------------
@router.get("/borrows")
def get_borrows():
    return _safe_forward("GET", f"{BORROW_SERVICE}/borrows")

@router.post("/borrows")
def create_borrow(payload: dict):
    return _safe_forward("POST", f"{BORROW_SERVICE}/borrows", payload)

@router.put("/borrows/{borrow_id}")
def update_borrow(borrow_id: str, payload: dict):
    return _safe_forward("PUT", f"{BORROW_SERVICE}/borrows/{borrow_id}", payload)

@router.delete("/borrows/{borrow_id}")
def delete_borrow(borrow_id: str):
    return _safe_forward("DELETE", f"{BORROW_SERVICE}/borrows/{borrow_id}")


# --------------- REVIEW SERVICE ROUTES ---------------
@router.get("/reviews")
def get_reviews():
    resp = requests.get(f"{REVIEW_SERVICE}/reviews")
    return resp.json()

@router.post("/reviews")
def create_review(payload: dict):
    resp = requests.post(f"{REVIEW_SERVICE}/reviews", json=payload)
    return resp.json()

@router.put("/reviews/{review_id}")
def update_review(review_id: str, payload: dict):
    resp = requests.put(f"{REVIEW_SERVICE}/reviews/{review_id}", json=payload)
    return resp.json()

@router.delete("/reviews/{review_id}")
def delete_review(review_id: str):
    resp = requests.delete(f"{REVIEW_SERVICE}/reviews/{review_id}")
    return resp.json()


# --------------- STAFF SERVICE ROUTES ---------------
@router.get("/staff")
def get_staff():
    resp = requests.get(f"{STAFF_SERVICE}/staff")
    return resp.json()

@router.post("/staff")
def create_staff(payload: dict):
    resp = requests.post(f"{STAFF_SERVICE}/staff", json=payload)
    return resp.json()

@router.put("/staff/{staff_id}")
def update_staff(staff_id: str, payload: dict):
    resp = requests.put(f"{STAFF_SERVICE}/staff/{staff_id}", json=payload)
    return resp.json()

@router.delete("/staff/{staff_id}")
def delete_staff(staff_id: str):
    resp = requests.delete(f"{STAFF_SERVICE}/staff/{staff_id}")
    return resp.json()

# ---------------- ROUTES ----------------

# ---------------- ENUM ----------------
class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


# ---------------- SCHEMAS ----------------
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


@router.get("/reservations")
def get_reservations():
    resp = requests.get(f"{RESERVATION_SERVICE}/reservations")
    return resp.json()


@router.post("/reservations")
def create_reservation(payload: ReservationCreate):
    # ✅ FIX: convert datetime → JSON-safe ISO strings
    data = payload.model_dump(mode="json")

    resp = requests.post(
        f"{RESERVATION_SERVICE}/reservations",
        json=data
    )

    return resp.json()


@router.put("/reservations/{reservation_id}")
def update_reservation(reservation_id: str, payload: ReservationUpdate):
    # ✅ FIX: only send updated fields + JSON safe format
    data = payload.model_dump(mode="json", exclude_unset=True)

    resp = requests.put(
        f"{RESERVATION_SERVICE}/reservations/{reservation_id}",
        json=data
    )

    return resp.json()


@router.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: str):
    resp = requests.delete(f"{RESERVATION_SERVICE}/reservations/{reservation_id}")
    return resp.json()