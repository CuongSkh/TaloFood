from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    phone: str | None = Field(default=None, max_length=30)
    role: str = 'CUSTOMER'
    is_active: bool = True

    @field_validator('full_name', 'email', 'phone', mode='before')
    @classmethod
    def strip_text(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator('email')
    @classmethod
    def normalize_email(cls, value: str):
        return value.casefold()

    @field_validator('role')
    @classmethod
    def validate_role(cls, value: str):
        value = value.strip().upper()
        if value not in {'CUSTOMER', 'ADMIN', 'SHIPPER'}:
            raise ValueError('Role không hợp lệ')
        return value

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str | None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PaginatedUserResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    size: int
    totalPages: int
