from fastapi import APIRouter,Depends,Header,Query,Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_active_user,require_admin
from app.models.user import User
from app.schemas.payment import PaymentListResponse,PaymentResponse,StripeSessionCreate,StripeSessionResponse,StripeVerifyResponse
from app.services.payment_service import PaymentService
router=APIRouter(prefix='/payments',tags=['Payments']); service=PaymentService()
@router.post('/stripe/create-session',response_model=StripeSessionResponse)
def create(payload:StripeSessionCreate,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)): return service.create_session(db,user,payload.order_id)
@router.get('/stripe/verify',response_model=StripeVerifyResponse)
def verify(session_id:str,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)): return service.verify(db,user,session_id)
@router.post('/stripe/cancel')
def cancel(payload:StripeSessionCreate,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)): return service.cancel_checkout(db,user,payload.order_id)
@router.post('/stripe/webhook')
async def webhook(request:Request,stripe_signature:str|None=Header(default=None),db:Session=Depends(get_db)): return service.webhook(db,await request.body(),stripe_signature or '')
@router.get('/order/{order_id}',response_model=list[PaymentResponse])
def order_payments(order_id:int,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)): return service.by_order(db,user,order_id)
