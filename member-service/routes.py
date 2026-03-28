from fastapi import APIRouter, HTTPException
from typing import List
from uuid import uuid4
from datetime import datetime
from db import member_collection, memory_members, DB_MODE
from models import MemberCreate, MemberUpdate, MemberResponse

router = APIRouter(prefix="/api/members", tags=["Members"])


def using_mongo() -> bool:
    return DB_MODE == "mongo" and member_collection is not None


def member_helper(member) -> dict:
    return {
        "id": str(member["_id"]),
        "member_code": member["member_code"],
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


# ── GET BY MEMBER CODE ────────────────────────────────────
@router.get("/{member_code}", response_model=MemberResponse)
def get_member(member_code: str):
    if using_mongo():
        member = member_collection.find_one({"member_code": member_code})
    else:
        member = next((m for m in memory_members.values() if m["member_code"] == member_code), None)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member_helper(member)


# ── CREATE ────────────────────────────────────────────────
@router.post("/", response_model=MemberResponse, status_code=201)
def create_member(member: MemberCreate):
    member_dict = member.model_dump()
    member_id = str(uuid4())
    member_dict["_id"] = member_id
    member_dict["registered_at"] = datetime.utcnow()

    if using_mongo():
        if member_collection.find_one({"email": member_dict["email"]}):
            raise HTTPException(status_code=400, detail=f"Email '{member_dict['email']}' already registered")
        if member_collection.find_one({"national_id": member_dict["national_id"]}):
            raise HTTPException(status_code=400, detail=f"National ID '{member_dict['national_id']}' already registered")
        if member_collection.find_one({"member_code": member_dict["member_code"]}):
            raise HTTPException(status_code=400, detail=f"Member code '{member_dict['member_code']}' already exists")
        member_collection.insert_one(member_dict)
    else:
        for m in memory_members.values():
            if m["email"] == member_dict["email"]:
                raise HTTPException(status_code=400, detail=f"Email '{member_dict['email']}' already registered")
            if m["national_id"] == member_dict["national_id"]:
                raise HTTPException(status_code=400, detail=f"National ID '{member_dict['national_id']}' already registered")
            if m["member_code"] == member_dict["member_code"]:
                raise HTTPException(status_code=400, detail=f"Member code '{member_dict['member_code']}' already exists")
        memory_members[member_id] = member_dict

    return member_helper(member_dict)


# ── UPDATE BY MEMBER CODE ─────────────────────────────────
@router.put("/{member_code}", response_model=MemberResponse)
def update_member(member_code: str, member: MemberUpdate):
    if using_mongo():
        existing = member_collection.find_one({"member_code": member_code})
    else:
        existing = next((m for m in memory_members.values() if m["member_code"] == member_code), None)

    if not existing:
        raise HTTPException(status_code=404, detail="Member not found")

    update_data = {k: v for k, v in member.model_dump().items() if v is not None}

    if using_mongo():
        if update_data:
            member_collection.update_one({"member_code": member_code}, {"$set": update_data})
        updated = member_collection.find_one({"member_code": member_code})
        return member_helper(updated)

    if update_data:
        existing.update(update_data)
    memory_members[existing["_id"]] = existing
    return member_helper(existing)


# ── DELETE BY MEMBER CODE ─────────────────────────────────
@router.delete("/{member_code}")
def delete_member(member_code: str):
    if using_mongo():
        result = member_collection.delete_one({"member_code": member_code})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Member not found")
        return {"message": "Member deleted successfully"}

    existing = next((m for m in memory_members.values() if m["member_code"] == member_code), None)
    if not existing:
        raise HTTPException(status_code=404, detail="Member not found")
    del memory_members[existing["_id"]]
    return {"message": "Member deleted successfully"}