from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime

from db import members_collection
from models import MemberCreate, MemberUpdate

router = APIRouter(
    prefix="/api/members",
    tags=["Members"]
)


# ── Helper ──────────────────────────────────────────────
def format_member(member) -> dict:
    """Convert MongoDB document to JSON-friendly dict."""
    member["id"] = str(member["_id"])
    del member["_id"]
    return member


def valid_object_id(member_id: str):
    """Validate MongoDB ObjectId format."""
    try:
        return ObjectId(member_id)
    except (InvalidId, Exception):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid member ID format: {member_id}"
        )


# ── CREATE ───────────────────────────────────────────────
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new library member"
)
def create_member(member: MemberCreate):
    # Check if email already exists
    existing = members_collection.find_one({"email": member.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{member.email}' is already registered"
        )

    # Check if national ID already exists
    existing_nid = members_collection.find_one({"national_id": member.national_id})
    if existing_nid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"National ID '{member.national_id}' is already registered"
        )

    new_member = member.dict()
    new_member["status"] = "active"
    new_member["registered_at"] = datetime.now().isoformat()
    new_member["updated_at"] = datetime.now().isoformat()

    result = members_collection.insert_one(new_member)
    created = members_collection.find_one({"_id": result.inserted_id})
    return format_member(created)


# ── READ ALL ─────────────────────────────────────────────
@router.get(
    "/",
    summary="Get all members"
)
def get_all_members():
    members = list(members_collection.find())
    return [format_member(m) for m in members]


# ── READ BY STATUS ───────────────────────────────────────
@router.get(
    "/status/{status}",
    summary="Get members by status (active / inactive / suspended)"
)
def get_members_by_status(status: str):
    allowed = ["active", "inactive", "suspended"]
    if status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Status must be one of {allowed}"
        )
    members = list(members_collection.find({"status": status}))
    return [format_member(m) for m in members]


# ── READ BY MEMBERSHIP TYPE ──────────────────────────────
@router.get(
    "/type/{membership_type}",
    summary="Get members by type (student / teacher / public)"
)
def get_members_by_type(membership_type: str):
    allowed = ["student", "teacher", "public"]
    if membership_type not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Membership type must be one of {allowed}"
        )
    members = list(members_collection.find({"membership_type": membership_type}))
    return [format_member(m) for m in members]


# ── READ ONE ─────────────────────────────────────────────
@router.get(
    "/{member_id}",
    summary="Get a single member by ID"
)
def get_member(member_id: str):
    oid = valid_object_id(member_id)
    member = members_collection.find_one({"_id": oid})
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with ID '{member_id}' not found"
        )
    return format_member(member)


# ── UPDATE ───────────────────────────────────────────────
@router.put(
    "/{member_id}",
    summary="Update member details"
)
def update_member(member_id: str, data: MemberUpdate):
    oid = valid_object_id(member_id)

    # Only update fields that were actually provided
    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided to update"
        )

    update_data["updated_at"] = datetime.now().isoformat()

    result = members_collection.update_one(
        {"_id": oid},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with ID '{member_id}' not found"
        )

    updated = members_collection.find_one({"_id": oid})
    return format_member(updated)


# ── SUSPEND ──────────────────────────────────────────────
@router.patch(
    "/{member_id}/suspend",
    summary="Suspend a member"
)
def suspend_member(member_id: str):
    oid = valid_object_id(member_id)
    result = members_collection.update_one(
        {"_id": oid},
        {"$set": {"status": "suspended", "updated_at": datetime.now().isoformat()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Member not found")
    member = members_collection.find_one({"_id": oid})
    return format_member(member)


# ── ACTIVATE ─────────────────────────────────────────────
@router.patch(
    "/{member_id}/activate",
    summary="Activate or reactivate a member"
)
def activate_member(member_id: str):
    oid = valid_object_id(member_id)
    result = members_collection.update_one(
        {"_id": oid},
        {"$set": {"status": "active", "updated_at": datetime.now().isoformat()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Member not found")
    member = members_collection.find_one({"_id": oid})
    return format_member(member)


# ── DELETE ───────────────────────────────────────────────
@router.delete(
    "/{member_id}",
    summary="Delete a member"
)
def delete_member(member_id: str):
    oid = valid_object_id(member_id)
    member = members_collection.find_one({"_id": oid})
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with ID '{member_id}' not found"
        )
    members_collection.delete_one({"_id": oid})
    return {"message": f"Member '{member['full_name']}' deleted successfully"}
