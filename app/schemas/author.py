from typing import Optional, TYPE_CHECKING
from datetime import date
from pydantic import BaseModel, Field, model_validator

if TYPE_CHECKING:
    from app.schemas.base_schema import BaseSchema, TimestampMixin


class AuthorBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Author's name"
        )

    date_of_birth: date = Field(..., description="Date of birth")
    date_of_death: Optional[date] = Field(
        None,
        description="Date of death"
        )

    biography: Optional[str] = Field(
        None,
        max_length=2000,
        description="Author's biography"
        )


class AuthorCreate(AuthorBase):
    @model_validator(mode="after")
    def validate_death_date(self) -> "AuthorCreate":
        if self.date_of_death and self.date_of_death <= self.date_of_birth:
            raise ValueError("Date of death must be later than date of birth")
        return self


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    date_of_birth: Optional[date] = None
    date_of_death: Optional[date] = None
    biography: Optional[str] = Field(None, max_length=2000)


class AuthorResponse(AuthorBase, TimestampMixin, BaseSchema):
    id: int
    slug: str
    books_count: Optional[int] = Field(
        None,
        description="Number of books by the author"
        )

    is_living: bool = Field(
        ...,
        description="Whether the author is alive"
        )
