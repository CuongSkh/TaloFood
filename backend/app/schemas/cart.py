from pydantic import BaseModel, Field

class CartItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=99)

class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0, le=99)

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    name: str
    description: str
    image_url: str
    unit_price: float
    quantity: int
    line_total: float
    available: bool

class CartResponse(BaseModel):
    id: int | None
    items: list[CartItemResponse]
    total_items: int
    total_quantity: int
    subtotal: float
    delivery_fee: float
    total_amount: float
