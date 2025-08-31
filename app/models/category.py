from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel, TimestampMixin
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .book import Book

class Category(BaseModel, TimestampMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False
        )
    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False
        )
    description: Mapped[str] = mapped_column(Text, nullable=True)

    books: Mapped[List["Book"]] = relationship(back_populates="category")
