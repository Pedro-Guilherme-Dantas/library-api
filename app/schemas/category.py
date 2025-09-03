from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from app.schemas.base_schema import BaseSchema, TimestampMixin


class CategoryBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Category name"
        )

    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Category description"
        )


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CategoryResponse(CategoryBase, TimestampMixin, BaseSchema):
    id: int
    slug: str
    books_count: Optional[int] = Field(
        None,
        description="Number of books in the category"
        )


class CategoryWithBooks(CategoryResponse):
    from app.schemas.book import BookResponse
    books: List['BookResponse'] = []
