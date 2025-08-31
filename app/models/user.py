from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel, TimestampMixin
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .loan import Loan

class User(BaseModel, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False
        )
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
        )
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
        )
    loans: Mapped[List["Loan"]] = relationship(back_populates="user")
