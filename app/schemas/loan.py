from typing import Optional, TYPE_CHECKING
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from app.schemas.base_schema import BaseSchema, TimestampMixin
    from app.schemas.user import UserResponse
    from app.schemas.book_copy import BookCopyResponse


class LoanStatusEnum(str, Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"


class LoanBase(BaseModel):
    user_id: int = Field(..., description="User ID")
    book_copy_id: int = Field(..., description="Book copy ID")
    due_date: datetime = Field(..., description="Due date")


class LoanCreate(BaseModel):
    user_id: int
    book_id: int = Field(..., description="Book ID")
    days: int = Field(14, ge=1, le=60, description="Loan days (default: 14)")


class LoanUpdate(BaseModel):
    due_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    status: Optional[LoanStatusEnum] = None


class LoanResponse(LoanBase, TimestampMixin, BaseSchema):
    id: int
    return_date: Optional[datetime]
    status: LoanStatusEnum
    user: UserResponse
    book_copy: BookCopyResponse
    is_overdue: bool = Field(..., description="Whether it is overdue")
    days_overdue: Optional[int] = Field(None, description="Days overdue")


class LoanReturn(BaseModel):
    return_date: Optional[datetime] = Field(
        None,
        description="Return date (default: now)"
        )
    condition_notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Condition notes at return"
        )
