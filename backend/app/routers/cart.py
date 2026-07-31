from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse
from app.services.cart_service import CartService
router=APIRouter(prefix='/cart',tags=['Cart']); service=CartService()
@router.get('',response_model=CartResponse)
def get_cart(db:Session=Depends(get_db),user:User=Depends(get_current_active_user)): return service.get(db,user.id)
@router.post('/items',response_model=CartResponse,status_code=status.HTTP_201_CREATED)
def add_item(payload:CartItemCreate,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)): return service.add(db,user.id,payload.product_id,payload.quantity)
@router.patch('/items/{item_id}',response_model=CartResponse)
def update_item(item_id:int,payload:CartItemUpdate,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)): return service.update(db,user.id,item_id,payload.quantity)
@router.delete('/items/{item_id}',response_model=CartResponse)
def remove_item(item_id:int,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)): return service.remove(db,user.id,item_id)
@router.delete('',response_model=CartResponse)
def clear_cart(db:Session=Depends(get_db),user:User=Depends(get_current_active_user)): return service.clear(db,user.id)
