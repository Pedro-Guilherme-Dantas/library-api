from typing import Optional, TYPE_CHECKING
from enum import Enum
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from app.schemas.base_schema import BaseSchema, TimestampMixin
    from app.schemas.book import BookResponse


class CopyStatusEnum(str, Enum):
    AVAILABLE = "available"
    LOANED = "loaned"
    DAMAGED = "damaged"
    LOST = "lost"


class BookCopyBase(BaseModel):
    book_id: int = Field(..., description="Book ID")
    condition_notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Condition notes"
        )

    status: CopyStatusEnum = Field(
        CopyStatusEnum.AVAILABLE,
        description="Copy status"
        )


class BookCopyCreate(BookCopyBase):
    pass


class BookCopyUpdate(BaseModel):
    condition_notes: Optional[str] = Field(None, max_length=500)
    status: Optional[CopyStatusEnum] = None


class BookCopyResponse(BookCopyBase, TimestampMixin, BaseSchema):
    id: int
    book: BookResponse
    is_available: bool = Field(
        ...,
        description="Whether it is available for loan"
        )
