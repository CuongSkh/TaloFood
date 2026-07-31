from datetime import date
from pydantic import BaseModel,Field
class OrderStatusUpdate(BaseModel): order_status:str
class OrderPaymentStatusUpdate(BaseModel): payment_status:str
class CategoryCreate(BaseModel): name:str=Field(min_length=2,max_length=100); slug:str=Field(min_length=2,max_length=120); description:str|None=None
class CategoryUpdate(BaseModel): name:str|None=Field(default=None,min_length=2,max_length=100); slug:str|None=Field(default=None,min_length=2,max_length=120); description:str|None=None
