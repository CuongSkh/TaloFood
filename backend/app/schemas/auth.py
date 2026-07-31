from pydantic import BaseModel, EmailStr, Field, field_validator
from app.schemas.user import UserResponse


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    phone: str | None = Field(default=None, max_length=30)

    @field_validator('full_name', 'email', 'phone', mode='before')
    @classmethod
    def strip_text(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator('email')
    @classmethod
    def normalize_email(cls, value: str):
        return value.casefold()


class LoginRequest(BaseModel):
    # Login accepts the project's local seeded admin address (admin@talofood.local).
    # Registration still uses EmailStr for normal customer email validation.
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=128)

    @field_validator('email')
    @classmethod
    def normalize_email(cls, value: str):
        normalized = value.strip().casefold()
        if '@' not in normalized or normalized.startswith('@') or normalized.endswith('@'):
            raise ValueError('Email không hợp lệ')
        return normalized


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: UserResponse
