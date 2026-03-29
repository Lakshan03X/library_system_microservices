from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class MembershipType(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    PUBLIC = "public"


class MemberStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class MemberCreate(BaseModel):
    member_id: str  # e.g. "MEM001"
    full_name: str
    email: str
    phone: str
    address: str
    membership_type: MembershipType
    national_id: str
    status: MemberStatus = MemberStatus.ACTIVE

    class Config:
        json_schema_extra = {
            "example": {
                "member_id": "1",
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
    membership_type: Optional[MembershipType] = None
    national_id: Optional[str] = None
    status: Optional[MemberStatus] = None

    class Config:
        json_schema_extra = {
            "example": {
                "member_id": "1",
                "full_name": "Kasun Perera",
                "email": "kasun@gmail.com",
                "phone": "0771234567",
                "address": "No 12, Galle Road, Colombo 03",
                "membership_type": "student",
                "national_id": "200012345678"
            }
        }


class MemberResponse(BaseModel):
    id: str
    member_id: str
    full_name: str
    email: str
    phone: str
    address: str
    membership_type: MembershipType
    national_id: str
    status: MemberStatus
    registered_at: datetime