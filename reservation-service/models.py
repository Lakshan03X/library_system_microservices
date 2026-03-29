from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class ReservationStatus(str, Enum):
    PENDING   = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    EXPIRED   = "expired"


class ReservationCreate(BaseModel):
    book_id: str
    member_id: str
    reserved_date: datetime = Field(default_factory=datetime.utcnow)
    expiry_date: datetime                                               # reservation expires if not picked up
    status: ReservationStatus = ReservationStatus.PENDING


class ReservationUpdate(BaseModel):
    book_id: Optional[str] = None
    member_id: Optional[str] = None
    reserved_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    confirmed_date: Optional[datetime] = None
    status: Optional[ReservationStatus] = None


class ReservationOut(BaseModel):
    id: str = Field(alias="_id")
    book_id: str
    member_id: str
    reserved_date: datetime
    expiry_date: datetime
    confirmed_date: Optional[datetime] = None
    status: ReservationStatus

    # ── Convert MongoDB ObjectId → str automatically ──────
    @field_validator("id", mode="before")
    @classmethod
    def convert_objectid(cls, v):
        return str(v)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }