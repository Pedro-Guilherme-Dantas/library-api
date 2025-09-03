from datetime import datetime
from pydantic import BaseModel


class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        validate_assignment = True
        use_enum_values = True
