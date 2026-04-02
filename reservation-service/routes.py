from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from uuid import uuid4
import os
import requests
from dotenv import load_dotenv
from db import reservation_collection, memory_reservations, DB_MODE
from models import ReservationCreate, ReservationUpdate, ReservationOut

load_dotenv()

router = APIRouter(prefix="/reservations", tags=["Reservations"])

# Service URLs for validation
BOOK_SERVICE = os.getenv("BOOK_SERVICE", "http://localhost:8081")
MEMBER_SERVICE = os.getenv("MEMBER_SERVICE", "http://localhost:8082")


def using_mongo() -> bool:
    return DB_MODE == "mongo" and reservation_collection is not None


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


def reservation_helper(reservation) -> dict:
    return {
        "id": str(reservation["_id"]),
        "book_id": reservation["book_id"],
        "member_id": reservation["member_id"],
        "reserved_date": reservation["reserved_date"],
        "expiry_date": reservation["expiry_date"],
        "confirmed_date": reservation.get("confirmed_date"),
        "status": reservation["status"]
    }


@router.get("/", response_model=List[ReservationOut])
def get_all_reservations():
    if using_mongo():
        return [reservation_helper(r) for r in reservation_collection.find()]
    return [reservation_helper(r) for r in memory_reservations.values()]


@router.get("/member/{member_id}", response_model=List[ReservationOut])
def get_reservations_by_member(member_id: str):
    if using_mongo():
        return [reservation_helper(r) for r in reservation_collection.find({"member_id": member_id})]
    return [reservation_helper(r) for r in memory_reservations.values() if r["member_id"] == member_id]


@router.get("/book/{book_id}", response_model=List[ReservationOut])
def get_reservations_by_book(book_id: str):
    if using_mongo():
        return [reservation_helper(r) for r in reservation_collection.find({"book_id": book_id})]
    return [reservation_helper(r) for r in memory_reservations.values() if r["book_id"] == book_id]


@router.get("/{reservation_id}", response_model=ReservationOut)
def get_reservation(reservation_id: str):
    if using_mongo():
        reservation = reservation_collection.find_one({"_id": reservation_id})
    else:
        reservation = memory_reservations.get(reservation_id)

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    return reservation_helper(reservation)


@router.post("/", response_model=ReservationOut)
def create_reservation(reservation: ReservationCreate):
    # Validate book exists
    if not validate_book_exists(reservation.book_id):
        raise HTTPException(status_code=400, detail=f"Book '{reservation.book_id}' not found in book service")
    
    # Validate member exists
    if not validate_member_exists(reservation.member_id):
        raise HTTPException(status_code=400, detail=f"Member '{reservation.member_id}' not found in member service")
    
    reservation_dict = reservation.model_dump()
    reservation_id = str(uuid4())
    reservation_dict["_id"] = reservation_id

    if using_mongo():
        reservation_collection.insert_one(reservation_dict)
    else:
        memory_reservations[reservation_id] = reservation_dict

    return reservation_helper(reservation_dict)


@router.put("/{reservation_id}", response_model=ReservationOut)
def update_reservation(reservation_id: str, reservation: ReservationUpdate):
    if using_mongo():
        existing = reservation_collection.find_one({"_id": reservation_id})
    else:
        existing = memory_reservations.get(reservation_id)

    if not existing:
        raise HTTPException(status_code=404, detail="Reservation not found")

    update_data = {k: v for k, v in reservation.model_dump().items() if v is not None}

    if using_mongo():
        if update_data:
            reservation_collection.update_one(
                {"_id": reservation_id},
                {"$set": update_data}
            )
        updated = reservation_collection.find_one({"_id": reservation_id})
        return reservation_helper(updated)

    if update_data:
        existing.update(update_data)
    memory_reservations[reservation_id] = existing
    return reservation_helper(existing)


@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: str):
    if using_mongo():
        result = reservation_collection.delete_one({"_id": reservation_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Reservation not found")
        return {"message": "Reservation deleted successfully"}

    if reservation_id not in memory_reservations:
        raise HTTPException(status_code=404, detail="Reservation not found")

    del memory_reservations[reservation_id]
    return {"message": "Reservation deleted successfully"}


@router.put("/{reservation_id}/confirm", response_model=ReservationOut)
def confirm_reservation(reservation_id: str):
    if using_mongo():
        existing = reservation_collection.find_one({"_id": reservation_id})
    else:
        existing = memory_reservations.get(reservation_id)

    if not existing:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if existing["status"] == "confirmed":
        raise HTTPException(status_code=400, detail="Already confirmed")

    update_payload = {
        "status": "confirmed",
        "confirmed_date": datetime.utcnow()
    }

    if using_mongo():
        reservation_collection.update_one(
            {"_id": reservation_id},
            {"$set": update_payload}
        )
        updated = reservation_collection.find_one({"_id": reservation_id})
        return reservation_helper(updated)

    existing.update(update_payload)
    memory_reservations[reservation_id] = existing
    return reservation_helper(existing)