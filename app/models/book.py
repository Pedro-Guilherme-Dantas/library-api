from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel, TimestampMixin
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .author import Author
    from .book_copy import BookCopy
    from .category import Category

class Book(BaseModel, TimestampMixin):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    isbn: Mapped[str] = mapped_column(
        String(13),
        unique=True,
        index=True,
        nullable=False
        )
    description: Mapped[str] = mapped_column(Text, nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False
        )
    category: Mapped["Category"] = relationship(back_populates="books")

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"),
        nullable=False
        )
    author: Mapped["Author"] = relationship(back_populates="books")

    book_copies: Mapped[List["BookCopy"]] = relationship(back_populates="book")
