from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from uuid import uuid4
from db import borrow_collection, memory_borrows, DB_MODE
from models import BorrowCreate, BorrowUpdate, BorrowResponse, BorrowStatus

router = APIRouter(prefix="/borrows", tags=["Borrows"])


def using_mongo() -> bool:
    return DB_MODE == "mongo" and borrow_collection is not None


def borrow_helper(borrow) -> dict:
    return {
        "id": str(borrow["_id"]),
        "book_id": borrow["book_id"],
        "member_id": borrow["member_id"],
        "borrow_date": borrow["borrow_date"],
        "due_date": borrow["due_date"],
        "return_date": borrow.get("return_date"),
        "status": borrow["status"]
    }


@router.get("/", response_model=List[BorrowResponse])
def get_all_borrows():
    if using_mongo():
        return [borrow_helper(borrow) for borrow in borrow_collection.find()]
    return [borrow_helper(borrow) for borrow in memory_borrows.values()]


@router.get("/member/{member_id}", response_model=List[BorrowResponse])
def get_borrows_by_member(member_id: str):
    if using_mongo():
        return [borrow_helper(borrow) for borrow in borrow_collection.find({"member_id": member_id})]
    return [borrow_helper(borrow) for borrow in memory_borrows.values() if borrow["member_id"] == member_id]


@router.get("/book/{book_id}", response_model=List[BorrowResponse])
def get_borrows_by_book(book_id: str):
    if using_mongo():
        return [borrow_helper(borrow) for borrow in borrow_collection.find({"book_id": book_id})]
    return [borrow_helper(borrow) for borrow in memory_borrows.values() if borrow["book_id"] == book_id]


@router.get("/{borrow_id}", response_model=BorrowResponse)
def get_borrow(borrow_id: str):
    if using_mongo():
        borrow = borrow_collection.find_one({"_id": borrow_id})
    else:
        borrow = memory_borrows.get(borrow_id)

    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    return borrow_helper(borrow)


@router.post("/", response_model=BorrowResponse)
def create_borrow(borrow: BorrowCreate):
    borrow_dict = borrow.model_dump()
    borrow_id = str(uuid4())
    borrow_dict["_id"] = borrow_id

    if using_mongo():
        borrow_collection.insert_one(borrow_dict)
    else:
        memory_borrows[borrow_id] = borrow_dict

    return borrow_helper(borrow_dict)


@router.put("/{borrow_id}", response_model=BorrowResponse)
def update_borrow(borrow_id: str, borrow: BorrowUpdate):
    if using_mongo():
        existing = borrow_collection.find_one({"_id": borrow_id})
    else:
        existing = memory_borrows.get(borrow_id)

    if not existing:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    
    update_data = {k: v for k, v in borrow.model_dump().items() if v is not None}

    if using_mongo():
        if update_data:
            borrow_collection.update_one(
                {"_id": borrow_id},
                {"$set": update_data}
            )
        updated_borrow = borrow_collection.find_one({"_id": borrow_id})
        return borrow_helper(updated_borrow)

    if update_data:
        existing.update(update_data)
    memory_borrows[borrow_id] = existing
    return borrow_helper(existing)


@router.delete("/{borrow_id}")
def delete_borrow(borrow_id: str):
    if using_mongo():
        result = borrow_collection.delete_one({"_id": borrow_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Borrow record not found")
        return {"message": "Borrow record deleted successfully"}

    if borrow_id not in memory_borrows:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    del memory_borrows[borrow_id]

    return {"message": "Borrow record deleted successfully"}


@router.put("/{borrow_id}/return", response_model=BorrowResponse)
def return_book(borrow_id: str):
    if using_mongo():
        existing = borrow_collection.find_one({"_id": borrow_id})
    else:
        existing = memory_borrows.get(borrow_id)

    if not existing:
        raise HTTPException(status_code=404, detail="Borrow record not found")

    if existing["status"] == BorrowStatus.RETURNED:
        raise HTTPException(status_code=400, detail="Book already returned")

    return_payload = {"status": BorrowStatus.RETURNED, "return_date": datetime.utcnow()}
    if using_mongo():
        borrow_collection.update_one(
            {"_id": borrow_id},
            {"$set": return_payload}
        )
        updated_borrow = borrow_collection.find_one({"_id": borrow_id})
        return borrow_helper(updated_borrow)

    existing.update(return_payload)
    memory_borrows[borrow_id] = existing
    return borrow_helper(existing)