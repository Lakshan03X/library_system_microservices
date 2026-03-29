from fastapi import APIRouter, HTTPException
from typing import List
from uuid import uuid4
from db import staff_collection, memory_staffs, DB_MODE
from models import StaffCreate, StaffUpdate, StaffResponse

router = APIRouter(prefix="/staffs", tags=["Staffs"])


def using_mongo():
    return DB_MODE == "mongo" and staff_collection is not None


def staff_helper(staff) -> dict:
    return {
        "id": str(staff["_id"]),
        "staff_id": staff["staff_id"],
        "name": staff["name"],
        "email": staff["email"],
        "role": staff["role"]
    }


@router.get("/", response_model=List[StaffResponse])
def get_all_staffs():
    if using_mongo():
        return [staff_helper(s) for s in staff_collection.find()]
    return [staff_helper(s) for s in memory_staffs.values()]


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: str):
    if using_mongo():
        staff = staff_collection.find_one({"staff_id": staff_id})
    else:
        staff = next((s for s in memory_staffs.values() if s["staff_id"] == staff_id), None)

    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")

    return staff_helper(staff)


@router.post("/", response_model=StaffResponse)
def create_staff(staff: StaffCreate):
    if using_mongo():
        existing = staff_collection.find_one({"staff_id": staff.staff_id})
    else:
        existing = next((s for s in memory_staffs.values() if s["staff_id"] == staff.staff_id), None)

    if existing:
        raise HTTPException(status_code=400, detail="Staff ID already exists")

    staff_dict = staff.model_dump()
    internal_id = str(uuid4())
    staff_dict["_id"] = internal_id

    if using_mongo():
        staff_collection.insert_one(staff_dict)
    else:
        memory_staffs[internal_id] = staff_dict

    return staff_helper(staff_dict)


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(staff_id: str, staff: StaffUpdate):
    if using_mongo():
        existing = staff_collection.find_one({"staff_id": staff_id})
    else:
        existing = next((s for s in memory_staffs.values() if s["staff_id"] == staff_id), None)

    if not existing:
        raise HTTPException(status_code=404, detail="Staff not found")

    update_data = {k: v for k, v in staff.model_dump().items() if v is not None}

    if using_mongo():
        if update_data:
            staff_collection.update_one({"staff_id": staff_id}, {"$set": update_data})
        updated = staff_collection.find_one({"staff_id": staff_id})
        return staff_helper(updated)

    existing.update(update_data)
    memory_staffs[existing["_id"]] = existing
    return staff_helper(existing)


@router.delete("/{staff_id}")
def delete_staff(staff_id: str):
    if using_mongo():
        result = staff_collection.delete_one({"staff_id": staff_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Staff not found")
        return {"message": "Staff deleted successfully"}

    existing = next((s for s in memory_staffs.values() if s["staff_id"] == staff_id), None)

    if not existing:
        raise HTTPException(status_code=404, detail="Staff not found")

    del memory_staffs[existing["_id"]]
    return {"message": "Staff deleted successfully"}