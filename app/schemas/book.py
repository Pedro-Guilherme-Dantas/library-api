from typing import Optional, TYPE_CHECKING
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

if TYPE_CHECKING:
    from app.schemas.base_schema import BaseSchema, TimestampMixin
    from app.schemas.category import CategoryResponse
    from app.schemas.author import AuthorResponse


class BookBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Book title"
    )

    isbn: str = Field(..., description="ISBN with 13 digits")

    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Book description"
    )

    year: int = Field(
        ...,
        ge=1000,
        le=datetime.now().year + 1,
        description="Publication year",
    )

    category_id: int = Field(..., description="Category ID")
    author_id: int = Field(..., description="Author ID")

    @field_validator("isbn")
    def validate_isbn(cls, v: str) -> str:
        if not v.isdigit() or len(v) != 13:
            raise ValueError("ISBN must contain exactly 13 digits")
        return v


class BookCreate(BookBase):
    @field_validator("isbn")
    def validate_isbn(cls, v: str) -> str:
        cleaned = v.replace("-", "").replace(" ", "")
        if not cleaned.isdigit() or len(cleaned) != 13:
            raise ValueError("ISBN must contain exactly 13 digits")
        return cleaned


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    isbn: Optional[str] = Field(None)
    description: Optional[str] = Field(None, max_length=2000)
    year: Optional[int] = Field(
        None,
        ge=1000,
        le=datetime.now().year + 1
    )

    category_id: Optional[int] = None
    author_id: Optional[int] = None

    @field_validator("isbn")
    def validate_isbn(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            cleaned = v.replace("-", "").replace(" ", "")
            if not cleaned.isdigit() or len(cleaned) != 13:
                raise ValueError("ISBN must contain exactly 13 digits")
            return cleaned
        return v


class BookResponse(BookBase, TimestampMixin, BaseSchema):
    id: int
    category: CategoryResponse
    author: AuthorResponse
    available_copies: int = Field(
        ...,
        description="Number of available copies"
    )

    total_copies: int = Field(
        ...,
        description="Total number of copies"
    )


class BookListResponse(BaseSchema):
    id: int
    title: str
    isbn: str
    year: int
    author_name: str
    category_name: str
    available_copies: int
    total_copies: int
