from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class BorrowStatus(str, Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"
    OVERDUE = "overdue"


class BorrowCreate(BaseModel):
    borrow_id: str
    book_id: List[str]
    member_id: str
    borrow_date: datetime = Field(default_factory=datetime.utcnow)
    due_date: datetime
    status: BorrowStatus = BorrowStatus.BORROWED


class BorrowUpdate(BaseModel):
    book_id: Optional[List[str]] = None
    member_id: Optional[str] = None
    borrow_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    status: Optional[BorrowStatus] = None


class BorrowResponse(BaseModel):
    id: str
    borrow_id: str
    book_id: List[str]
    member_id: str
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: BorrowStatus