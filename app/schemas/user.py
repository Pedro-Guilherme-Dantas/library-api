from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, EmailStr, Field, field_validator

if TYPE_CHECKING:
    from app.schemas.base_schema import BaseSchema, TimestampMixin


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User email")
    username: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Username"
        )

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name"
        )


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password"
        )

    is_admin: bool = Field(
        False,
        description="Whether the user is an administrator"
        )

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError(
                "Password must contain at least one uppercase letter"
                )
        if not any(c.islower() for c in v):
            raise ValueError(
                "Password must contain at least one lowercase letter"
                )
        if not any(c.isdigit() for c in v):
            raise ValueError(
                "Password must contain at least one number"
                )
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    is_admin: Optional[bool] = None


class UserResponse(UserBase, TimestampMixin, BaseSchema):
    id: int
    is_admin: bool
    active_loans_count: int = Field(..., description="Number of active loans")


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
