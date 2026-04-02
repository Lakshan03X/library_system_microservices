from fastapi import APIRouter, HTTPException
from typing import List
from uuid import uuid4
from datetime import datetime
from db import member_collection, memory_members, DB_MODE
from models import MemberCreate, MemberUpdate, MemberResponse

router = APIRouter(prefix="/members", tags=["Members"])


def using_mongo() -> bool:
    return DB_MODE == "mongo" and member_collection is not None


def member_helper(member) -> dict:
    return {
        "id": str(member["_id"]),
        "member_id": member["member_id"],
        "full_name": member["full_name"],
        "email": member["email"],
        "phone": member["phone"],
        "address": member["address"],
        "membership_type": member["membership_type"],
        "national_id": member["national_id"],
        "status": member["status"],
        "registered_at": member["registered_at"]
    }


# ── GET ALL ───────────────────────────────────────────────
@router.get("/", response_model=List[MemberResponse])
def get_all_members():
    if using_mongo():
        return [member_helper(m) for m in member_collection.find()]
    return [member_helper(m) for m in memory_members.values()]


# ── GET BY MEMBER ID ──────────────────────────────────────
@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: str):
    if using_mongo():
        member = member_collection.find_one({"member_id": member_id})
    else:
        member = next((m for m in memory_members.values() if m["member_id"] == member_id), None)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member_helper(member)


# ── CREATE ────────────────────────────────────────────────
@router.post("/", response_model=MemberResponse, status_code=201)
def create_member(member: MemberCreate):
    member_dict = member.model_dump()
    member_dict["_id"] = str(uuid4())  # internal MongoDB _id (hidden from user)
    member_dict["registered_at"] = datetime.utcnow()

    if using_mongo():
        if member_collection.find_one({"member_id": member_dict["member_id"]}):
            raise HTTPException(status_code=400, detail=f"Member ID '{member_dict['member_id']}' already exists")
        if member_collection.find_one({"email": member_dict["email"]}):
            raise HTTPException(status_code=400, detail=f"Email '{member_dict['email']}' already registered")
        if member_collection.find_one({"national_id": member_dict["national_id"]}):
            raise HTTPException(status_code=400, detail=f"National ID '{member_dict['national_id']}' already registered")
        member_collection.insert_one(member_dict)
    else:
        for m in memory_members.values():
            if m["member_id"] == member_dict["member_id"]:
                raise HTTPException(status_code=400, detail=f"Member ID '{member_dict['member_id']}' already exists")
            if m["email"] == member_dict["email"]:
                raise HTTPException(status_code=400, detail=f"Email '{member_dict['email']}' already registered")
            if m["national_id"] == member_dict["national_id"]:
                raise HTTPException(status_code=400, detail=f"National ID '{member_dict['national_id']}' already registered")
        memory_members[member_dict["_id"]] = member_dict

    return member_helper(member_dict)


# ── UPDATE BY MEMBER ID ───────────────────────────────────
@router.put("/{member_id}", response_model=MemberResponse)
def update_member(member_id: str, member: MemberUpdate):
    if using_mongo():
        existing = member_collection.find_one({"member_id": member_id})
    else:
        existing = next((m for m in memory_members.values() if m["member_id"] == member_id), None)

    if not existing:
        raise HTTPException(status_code=404, detail="Member not found")

    update_data = {k: v for k, v in member.model_dump().items() if v is not None}

    if using_mongo():
        if update_data:
            member_collection.update_one({"member_id": member_id}, {"$set": update_data})
        updated = member_collection.find_one({"member_id": member_id})
        return member_helper(updated)

    if update_data:
        existing.update(update_data)
    memory_members[existing["_id"]] = existing
    return member_helper(existing)


# ── DELETE BY MEMBER ID ───────────────────────────────────
@router.delete("/{member_id}")
def delete_member(member_id: str):
    if using_mongo():
        result = member_collection.delete_one({"member_id": member_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Member not found")
        return {"message": "Member deleted successfully"}

    existing = next((m for m in memory_members.values() if m["member_id"] == member_id), None)
    if not existing:
        raise HTTPException(status_code=404, detail="Member not found")
    del memory_members[existing["_id"]]
    return {"message": "Member deleted successfully"}
