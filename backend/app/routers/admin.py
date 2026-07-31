from fastapi import APIRouter,Depends,HTTPException,Query,status
from sqlalchemy import func,or_,select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import require_admin
from app.models.category import Category
from app.models.product import Product
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.schemas.admin import CategoryCreate,CategoryUpdate,OrderPaymentStatusUpdate,OrderStatusUpdate
from app.schemas.category import CategoryResponse
from app.schemas.payment import PaymentListResponse,PaymentResponse
from app.services.admin_service import AdminService
from app.services.payment_service import PaymentService
from app.services.user_service import UserService
router=APIRouter(prefix='/admin',tags=['Admin']); service=AdminService(); payments=PaymentService(); users=UserService(); cats=CategoryRepository()
@router.get('/stats/overview')
def overview(db:Session=Depends(get_db),_:User=Depends(require_admin)):return service.overview(db)
@router.get('/stats/monthly-revenue')
def monthly(db:Session=Depends(get_db),_:User=Depends(require_admin)):return service.monthly(db)
@router.get('/stats/recent-orders')
def recent(limit:int=Query(8,ge=1,le=30),db:Session=Depends(get_db),_:User=Depends(require_admin)):return service.recent(db,limit)
@router.get('/stats/top-products')
def top(limit:int=Query(5,ge=1,le=20),db:Session=Depends(get_db),_:User=Depends(require_admin)):return service.top_products(db,limit)
@router.get('/stats/order-status')
def status_stats(db:Session=Depends(get_db),_:User=Depends(require_admin)):return service.status_stats(db)
@router.get('/orders')
def orders(page:int=1,size:int=20,search:str|None=None,order_status:str|None=None,payment_status:str|None=None,payment_method:str|None=None,db:Session=Depends(get_db),_:User=Depends(require_admin)):return service.orders(db,page,size,search,order_status,payment_status,payment_method)
@router.get('/orders/{oid}')
def order(oid:int,db:Session=Depends(get_db),_:User=Depends(require_admin)):return service.order_dict(service.get_order(db,oid))
@router.patch('/orders/{oid}/status')
def update_order(oid:int,payload:OrderStatusUpdate,db:Session=Depends(get_db),_:User=Depends(require_admin)):return service.update_order(db,oid,payload.order_status)
@router.patch('/orders/{oid}/payment-status')
def update_payment(oid:int,payload:OrderPaymentStatusUpdate,db:Session=Depends(get_db),_:User=Depends(require_admin)):return service.update_payment(db,oid,payload.payment_status)
@router.get('/users')
def list_users(page:int=1,size:int=20,search:str|None=None,role:str|None=None,is_active:bool|None=None,db:Session=Depends(get_db),_:User=Depends(require_admin)):
    q=select(User)
    if search:q=q.where(or_(User.full_name.ilike(f'%{search}%'),User.email.ilike(f'%{search}%')))
    if role:q=q.where(User.role==role)
    if is_active is not None:q=q.where(User.is_active==is_active)
    total=db.scalar(select(func.count()).select_from(q.subquery())) or 0; items=db.scalars(q.order_by(User.created_at.desc()).offset((page-1)*size).limit(size)).all()
    return {'items':[{'id':u.id,'full_name':u.full_name,'email':u.email,'phone':u.phone,'role':u.role,'is_active':u.is_active,'created_at':u.created_at,'updated_at':u.updated_at} for u in items],'total':total,'page':page,'size':size,'totalPages':__import__('math').ceil(total/size) if total else 0}
@router.get('/users/{uid}')
def get_user(uid:int,db:Session=Depends(get_db),_:User=Depends(require_admin)):
    u=db.get(User,uid)
    if not u:raise HTTPException(404,'Không tìm thấy người dùng')
    return {'id':u.id,'full_name':u.full_name,'email':u.email,'phone':u.phone,'role':u.role,'is_active':u.is_active,'created_at':u.created_at,'updated_at':u.updated_at}
@router.get('/payments',response_model=PaymentListResponse)
def list_payments(page:int=1,size:int=20,provider:str|None=None,status:str|None=None,order_code:str|None=None,db:Session=Depends(get_db),_:User=Depends(require_admin)):return payments.admin_list(db,page,size,provider,status,order_code)
@router.get('/payments/{pid}',response_model=PaymentResponse)
def payment(pid:int,db:Session=Depends(get_db),_:User=Depends(require_admin)):
    from app.models.payment import Payment
    p=db.get(Payment,pid)
    if not p:raise HTTPException(404,'Không tìm thấy thanh toán')
    return payments._resp(p)
@router.post('/categories',response_model=CategoryResponse,status_code=201)
def create_category(payload:CategoryCreate,db:Session=Depends(get_db),_:User=Depends(require_admin)):
    if db.scalar(select(Category).where(or_(Category.name==payload.name,Category.slug==payload.slug))):raise HTTPException(409,'Danh mục đã tồn tại')
    c=Category(**payload.model_dump());db.add(c);db.commit();db.refresh(c);return c
@router.put('/categories/{cid}',response_model=CategoryResponse)
def update_category(cid:int,payload:CategoryUpdate,db:Session=Depends(get_db),_:User=Depends(require_admin)):
    c=db.get(Category,cid)
    if not c:raise HTTPException(404,'Không tìm thấy danh mục')
    for k,v in payload.model_dump(exclude_unset=True).items():setattr(c,k,v)
    db.commit();db.refresh(c);return c
@router.delete('/categories/{cid}')
def delete_category(cid:int,db:Session=Depends(get_db),_:User=Depends(require_admin)):
    c=db.get(Category,cid)
    if not c:raise HTTPException(404,'Không tìm thấy danh mục')
    if db.scalar(select(func.count(Product.id)).where(Product.category_id==cid)):raise HTTPException(409,'Không thể xóa danh mục đang có món ăn')
    db.delete(c);db.commit();return {'message':'Đã xóa danh mục'}
