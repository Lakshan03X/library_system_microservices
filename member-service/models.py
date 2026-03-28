from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class MembershipType(str, Enum):
    student = "student"
    teacher = "teacher"
    public = "public"


class MemberStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"


# Used when CREATING a new member (no id needed)
class MemberCreate(BaseModel):
    full_name: str
    email: str
    phone: str
    address: str
    membership_type: MembershipType
    national_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Kasun Perera",
                "email": "kasun@gmail.com",
                "phone": "0771234567",
                "address": "No 12, Galle Road, Colombo 03",
                "membership_type": "student",
                "national_id": "200012345678"
            }
        }


# Used when UPDATING a member (all fields optional)
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
                "phone": "0779876543",
                "address": "No 5, Kandy Road, Colombo 10",
                "status": "active"
            }
        }
