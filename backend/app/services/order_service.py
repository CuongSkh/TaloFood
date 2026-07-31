import math
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session, joinedload
from app.core.config import DELIVERY_FEE
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem

class OrderService:
    def _response(self,o):
        return {'id':o.id,'order_code':o.order_code,'receiver_name':o.receiver_name,'receiver_phone':o.receiver_phone,'delivery_address':o.delivery_address,'note':o.note,'subtotal':float(o.subtotal),'delivery_fee':float(o.delivery_fee),'discount_amount':float(o.discount_amount),'total_amount':float(o.total_amount),'payment_method':o.payment_method,'payment_status':o.payment_status,'order_status':o.order_status,'cancel_reason':o.cancel_reason,'cancelled_at':o.cancelled_at,'created_at':o.created_at,'updated_at':o.updated_at,'total_quantity':sum(i.quantity for i in o.items),'items':[{'id':i.id,'product_id':i.product_id,'product_name':i.product_name,'product_image_url':i.product_image_url,'unit_price':float(i.unit_price),'quantity':i.quantity,'line_total':float(i.line_total)} for i in o.items]}
    def _get(self,db,order_id): return db.execute(select(Order).options(joinedload(Order.items)).where(Order.id==order_id)).unique().scalar_one_or_none()
    def create(self,db,user_id,payload):
        try:
            cart=db.execute(select(Cart).options(joinedload(Cart.items).joinedload(CartItem.product)).where(Cart.user_id==user_id)).unique().scalar_one_or_none()
            if not cart or not cart.items: raise HTTPException(400,'Giỏ hàng của bạn đang trống')
            subtotal=Decimal('0')
            for ci in cart.items:
                if not ci.product or not ci.product.available: raise HTTPException(409,f'Món {ci.product.name if ci.product else ci.product_id} hiện không còn phục vụ')
                subtotal += ci.product.price*ci.quantity
            order=Order(order_code=f"TF{datetime.now():%Y%m%d}{uuid4().hex[:8].upper()}",user_id=user_id,receiver_name=payload.receiver_name,receiver_phone=payload.receiver_phone,delivery_address=payload.delivery_address,note=payload.note,subtotal=subtotal,delivery_fee=DELIVERY_FEE,discount_amount=0,total_amount=subtotal+DELIVERY_FEE,payment_method='COD',payment_status='UNPAID',order_status='PENDING')
            db.add(order); db.flush()
            for ci in cart.items:
                p=ci.product; line=p.price*ci.quantity
                db.add(OrderItem(order_id=order.id,product_id=p.id,product_name=p.name,product_image_url=p.image_url,unit_price=p.price,quantity=ci.quantity,line_total=line))
            db.execute(delete(CartItem).where(CartItem.cart_id==cart.id)); db.commit()
            return self._response(self._get(db,order.id))
        except HTTPException:
            db.rollback(); raise
        except Exception:
            db.rollback(); raise
    def list(self,db,user_id,page,size,status_filter=None):
        filters=[Order.user_id==user_id]
        if status_filter: filters.append(Order.order_status==status_filter)
        total=db.scalar(select(func.count(Order.id)).where(*filters)) or 0
        orders=db.execute(select(Order).options(joinedload(Order.items)).where(*filters).order_by(Order.created_at.desc()).offset((page-1)*size).limit(size)).unique().scalars().all()
        return {'items':[self._response(o) for o in orders],'total':total,'page':page,'size':size,'totalPages':math.ceil(total/size) if total else 0}
    def detail(self,db,user,order_id):
        order=self._get(db,order_id)
        if not order: raise HTTPException(404,'Không tìm thấy đơn hàng')
        if order.user_id!=user.id and user.role!='ADMIN': raise HTTPException(403,'Bạn không có quyền xem đơn hàng này')
        return self._response(order)
    def cancel(self,db,user_id,order_id,reason):
        order=self._get(db,order_id)
        if not order: raise HTTPException(404,'Không tìm thấy đơn hàng')
        if order.user_id!=user_id: raise HTTPException(403,'Bạn không có quyền hủy đơn hàng này')
        if order.order_status not in {'PENDING','CONFIRMED'}: raise HTTPException(409,'Không thể hủy đơn hàng ở trạng thái hiện tại')
        order.order_status='CANCELLED'; order.cancel_reason=reason; order.cancelled_at=datetime.now(timezone.utc); db.commit()
        return self._response(self._get(db,order_id))
