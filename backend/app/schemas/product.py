from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.core.config import CATEGORIES

Name = Annotated[str, Field(min_length=3, max_length=100)]
Description = Annotated[str, Field(min_length=10, max_length=1000)]

class ProductBase(BaseModel):
    name: Name
    price: float = Field(gt=0)
    category: str
    description: Description
    imageUrl: str = "/images/placeholder.svg"
    badge: str | None = Field(default=None, max_length=50)
    featured: bool = False
    isNew: bool = False
    available: bool = True
    objectPosition: str = Field(default="center", max_length=100)

    @field_validator("name", "description", "imageUrl", "badge", "objectPosition", mode="before")
    @classmethod
    def strip_text(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("category", mode="before")
    @classmethod
    def validate_category(cls, value):
        value = value.strip() if isinstance(value, str) else value
        if value not in CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(CATEGORIES)}")
        return value

    @field_validator("imageUrl")
    @classmethod
    def validate_image_url(cls, value: str):
        if not value:
            return "/images/placeholder.svg"
        if value.startswith(("/images/", "http://", "https://")):
            return value
        raise ValueError("imageUrl must be an absolute URL or start with /images/")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Name | None = None
    price: float | None = Field(default=None, gt=0)
    category: str | None = None
    description: Description | None = None
    imageUrl: str | None = None
    badge: str | None = Field(default=None, max_length=50)
    featured: bool | None = None
    isNew: bool | None = None
    available: bool | None = None
    objectPosition: str | None = Field(default=None, max_length=100)

    @field_validator("name", "description", "imageUrl", "badge", "objectPosition", mode="before")
    @classmethod
    def strip_text(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("category", mode="before")
    @classmethod
    def validate_category(cls, value):
        if value is None:
            return value
        value = value.strip()
        if value not in CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(CATEGORIES)}")
        return value

    @field_validator("imageUrl")
    @classmethod
    def validate_image_url(cls, value):
        if value is None:
            return value
        if value.startswith(("/images/", "http://", "https://")):
            return value
        raise ValueError("imageUrl must be an absolute URL or start with /images/")

class ProductResponse(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PaginatedProductResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    size: int
    totalPages: int

class DeleteProductResponse(BaseModel):
    message: str

class ImageUploadResponse(BaseModel):
    imageUrl: str
