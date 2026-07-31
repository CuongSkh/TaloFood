from datetime import datetime
from pydantic import BaseModel, Field
class StripeSessionCreate(BaseModel): order_id:int=Field(gt=0)
class StripeSessionResponse(BaseModel): payment_id:int; session_id:str; checkout_url:str
class StripeVerifyResponse(BaseModel): payment_id:int; order_id:int; order_code:str; amount:float; currency:str; payment_status:str; order_payment_status:str
class PaymentResponse(BaseModel):
    id:int; order_id:int; provider:str; provider_session_id:str|None; transaction_id:str|None; amount:float; currency:str; status:str; checkout_url:str|None; failure_reason:str|None; paid_at:datetime|None; created_at:datetime; updated_at:datetime
class PaymentListResponse(BaseModel): items:list[PaymentResponse]; total:int; page:int; size:int; totalPages:int
