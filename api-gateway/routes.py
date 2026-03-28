import os
import requests
from fastapi import APIRouter
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
    resp = requests.get(f"{BORROW_SERVICE}/borrows")
    return resp.json()

@router.post("/borrows")
def create_borrow(payload: dict):
    resp = requests.post(f"{BORROW_SERVICE}/borrows", json=payload)
    return resp.json()

@router.put("/borrows/{borrow_id}")
def update_borrow(borrow_id: str, payload: dict):
    resp = requests.put(f"{BORROW_SERVICE}/borrows/{borrow_id}", json=payload)
    return resp.json()

@router.delete("/borrows/{borrow_id}")
def delete_borrow(borrow_id: str):
    resp = requests.delete(f"{BORROW_SERVICE}/borrows/{borrow_id}")
    return resp.json()


# --------------- REVIEW SERVICE ROUTES ---------------
@router.get("/reviews")
def get_all_reviews():
    resp = requests.get(f"{REVIEW_SERVICE}/reviews/")
    return resp.json()

@router.get("/reviews/book/{book_id}")
def get_reviews_by_book(book_id: str):
    resp = requests.get(f"{REVIEW_SERVICE}/reviews/book/{book_id}")
    return resp.json()

@router.get("/reviews/member/{member_id}")
def get_reviews_by_member(member_id: str):
    resp = requests.get(f"{REVIEW_SERVICE}/reviews/member/{member_id}")
    return resp.json()

@router.get("/reviews/{review_id}")
def get_review(review_id: str):
    resp = requests.get(f"{REVIEW_SERVICE}/reviews/{review_id}")
    return resp.json()

@router.post("/reviews")
def create_review(payload: dict):
    resp = requests.post(f"{REVIEW_SERVICE}/reviews/", json=payload)
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


# --------------- RESERVATION SERVICE ROUTES ---------------
@router.get("/reservations")
def get_reservations():
    resp = requests.get(f"{RESERVATION_SERVICE}/reservations")
    return resp.json()

@router.post("/reservations")
def create_reservation(payload: dict):
    resp = requests.post(f"{RESERVATION_SERVICE}/reservations", json=payload)
    return resp.json()

@router.put("/reservations/{reservation_id}")
def update_reservation(reservation_id: str, payload: dict):
    resp = requests.put(f"{RESERVATION_SERVICE}/reservations/{reservation_id}", json=payload)
    return resp.json()

@router.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: str):
    resp = requests.delete(f"{RESERVATION_SERVICE}/reservations/{reservation_id}")
    return resp.json()