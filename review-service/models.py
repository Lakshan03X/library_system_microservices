from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReviewCreate(BaseModel):
    book_id: str
    member_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    review_date: datetime = Field(default_factory=datetime.utcnow)


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
    review_date: Optional[datetime] = None


class ReviewResponse(BaseModel):
    id: str
    book_id: str
    member_id: str
    rating: int
    comment: Optional[str] = None
    review_date: datetime