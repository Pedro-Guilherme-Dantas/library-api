from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel, TimestampMixin
from typing import List, TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from .book import Book
    from .loan import Loan

class CopyStatus(enum.Enum):
    AVAILABLE = "available"
    LOANED = "loaned"
    LOST = "lost"
    DAMAGED = "damaged"

class BookCopy(BaseModel, TimestampMixin):
    __tablename__ = "book_copies"

    status: Mapped["CopyStatus"] = mapped_column(
        Enum(CopyStatus),
        default=CopyStatus.AVAILABLE,
        nullable=False
        )
    condition_notes: Mapped[str] = mapped_column(Text, nullable=True)

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        nullable=False
        )
    book: Mapped["Book"] = relationship(back_populates="book_copies")

    loans: Mapped[List["Loan"]] = relationship(back_populates="book_copy")
