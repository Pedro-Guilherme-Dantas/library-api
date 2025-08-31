from sqlalchemy import Enum, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel, TimestampMixin
from typing import TYPE_CHECKING
from datetime import datetime
import enum

if TYPE_CHECKING:
    from .user import User
    from .book_copy import BookCopy

class LoanStatus(enum.Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"

class Loan(BaseModel, TimestampMixin):
    __tablename__ = "loans"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="loans")

    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    return_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
        )
    status: Mapped["LoanStatus"] = mapped_column(
        Enum(LoanStatus),
        default=LoanStatus.ACTIVE,
        nullable=False
        )

    book_copy_id: Mapped[int] = mapped_column(ForeignKey("book_copies.id"))
    book_copy: Mapped["BookCopy"] = relationship(back_populates="loans")
