from pydantic import BaseModel
from typing import Optional


class StaffCreate(BaseModel):
    staff_id: str
    name: str
    email: str
    role: str


class StaffUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None


class StaffResponse(BaseModel):
    id: str
    staff_id: str
    name: str
    email: str
    role: str