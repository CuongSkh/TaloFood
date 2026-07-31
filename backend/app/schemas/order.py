from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class OrderCreate(BaseModel):
    receiver_name: str = Field(min_length=2, max_length=120)
    receiver_phone: str = Field(min_length=8, max_length=30)
    delivery_address: str = Field(min_length=10, max_length=500)
    note: str | None = Field(default=None, max_length=1000)
    payment_method: str = 'COD'
    @field_validator('receiver_name','receiver_phone','delivery_address','note', mode='before')
    @classmethod
    def strip_text(cls, value): return value.strip() if isinstance(value, str) else value
    @field_validator('payment_method')
    @classmethod
    def validate_method(cls, value):
        value = value.upper()
        if value not in {'COD','STRIPE'}: raise ValueError('Chỉ hỗ trợ COD hoặc STRIPE')
        return value

class OrderCancel(BaseModel):
    cancel_reason: str | None = Field(default=None, max_length=500)

class OrderItemResponse(BaseModel):
    id: int
    product_id: int | None
    product_name: str
    product_image_url: str
    unit_price: float
    quantity: int
    line_total: float

class OrderResponse(BaseModel):
    id: int
    order_code: str
    receiver_name: str
    receiver_phone: str
    delivery_address: str
    note: str | None
    subtotal: float
    delivery_fee: float
    discount_amount: float
    total_amount: float
    payment_method: str
    payment_status: str
    order_status: str
    cancel_reason: str | None
    cancelled_at: datetime | None
    created_at: datetime
    updated_at: datetime
    total_quantity: int
    items: list[OrderItemResponse]

class OrderListResponse(BaseModel):
    items: list[OrderResponse]
    total: int
    page: int
    size: int
    totalPages: int
