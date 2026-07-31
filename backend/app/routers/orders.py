from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.order import OrderCancel, OrderCreate, OrderListResponse, OrderResponse
from app.services.order_service import OrderService
router=APIRouter(prefix='/orders',tags=['Orders']); service=OrderService()
@router.post('',response_model=OrderResponse,status_code=status.HTTP_201_CREATED)
def create_order(payload:OrderCreate,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)): return service.create(db,user.id,payload)
@router.get('/me',response_model=OrderListResponse)
def my_orders(page:int=Query(1,ge=1),size:int=Query(10,ge=1,le=100),order_status:str|None=None,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)): return service.list(db,user.id,page,size,order_status)
@router.get('/{order_id}',response_model=OrderResponse)
def order_detail(order_id:int,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)): return service.detail(db,user,order_id)
@router.patch('/{order_id}/cancel',response_model=OrderResponse)
def cancel_order(order_id:int,payload:OrderCancel,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)): return service.cancel(db,user.id,order_id,payload.cancel_reason)
