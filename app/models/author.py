from datetime import date
from sqlalchemy import String, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel, TimestampMixin
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .book import Book

class Author(BaseModel, TimestampMixin):
    __tablename__ = "authors"

    name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    slug: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        index=True,
        nullable=False
        )

    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    date_of_death: Mapped[date] = mapped_column(Date, nullable=True)

    books: Mapped[List["Book"]] = relationship(back_populates="author")

    biography: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
