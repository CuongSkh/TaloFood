import math
from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import case,func,or_,select
from sqlalchemy.orm import Session,joinedload
from app.models.category import Category
from app.models.order import Order,OrderItem
from app.models.payment import Payment
from app.models.product import Product
from app.models.user import User

class AdminService:
    transitions={'PENDING':{'CONFIRMED','CANCELLED'},'CONFIRMED':{'PREPARING','CANCELLED'},'PREPARING':{'DELIVERING'},'DELIVERING':{'COMPLETED'},'COMPLETED':set(),'CANCELLED':set()}
    def overview(self,db):
        revenue=db.scalar(select(func.coalesce(func.sum(Order.total_amount),0)).where(Order.payment_status=='PAID',Order.order_status!='CANCELLED')) or 0
        return {'total_products':db.scalar(select(func.count(Product.id))) or 0,'total_orders':db.scalar(select(func.count(Order.id))) or 0,'total_users':db.scalar(select(func.count(User.id))) or 0,'total_revenue':float(revenue)}
    def monthly(self,db):
        rows=db.execute(select(func.to_char(Order.created_at,'YYYY-MM').label('month'),func.sum(Order.total_amount)).where(Order.payment_status=='PAID',Order.order_status!='CANCELLED').group_by('month').order_by('month')).all()
        return [{'month':m,'revenue':float(v)} for m,v in rows]
    def recent(self,db,limit=8):
        rows=db.scalars(select(Order).options(joinedload(Order.items)).order_by(Order.created_at.desc()).limit(limit)).unique().all()
        return [self.order_dict(o) for o in rows]
    def top_products(self,db,limit=5):
        rows=db.execute(select(OrderItem.product_name,func.sum(OrderItem.quantity),func.sum(OrderItem.line_total)).join(Order).where(Order.order_status!='CANCELLED').group_by(OrderItem.product_name).order_by(func.sum(OrderItem.quantity).desc()).limit(limit)).all()
        return [{'product_name':n,'quantity':int(q or 0),'revenue':float(r or 0)} for n,q,r in rows]
    def status_stats(self,db):
        return [{'status':s,'count':c} for s,c in db.execute(select(Order.order_status,func.count(Order.id)).group_by(Order.order_status)).all()]
    def order_dict(self,o):
        return {'id':o.id,'order_code':o.order_code,'user_id':o.user_id,'receiver_name':o.receiver_name,'receiver_phone':o.receiver_phone,'delivery_address':o.delivery_address,'note':o.note,'subtotal':float(o.subtotal),'delivery_fee':float(o.delivery_fee),'discount_amount':float(o.discount_amount),'total_amount':float(o.total_amount),'payment_method':o.payment_method,'payment_status':o.payment_status,'order_status':o.order_status,'created_at':o.created_at,'updated_at':o.updated_at,'items':[{'id':i.id,'product_name':i.product_name,'product_image_url':i.product_image_url,'unit_price':float(i.unit_price),'quantity':i.quantity,'line_total':float(i.line_total)} for i in o.items]}
    def orders(self,db,page,size,search=None,order_status=None,payment_status=None,payment_method=None):
        q=select(Order).options(joinedload(Order.items))
        if search:q=q.where(or_(Order.order_code.ilike(f'%{search}%'),Order.receiver_name.ilike(f'%{search}%')))
        if order_status:q=q.where(Order.order_status==order_status)
        if payment_status:q=q.where(Order.payment_status==payment_status)
        if payment_method:q=q.where(Order.payment_method==payment_method)
        count=select(func.count()).select_from(q.order_by(None).subquery()); total=db.scalar(count) or 0
        items=db.execute(q.order_by(Order.created_at.desc()).offset((page-1)*size).limit(size)).unique().scalars().all()
        return {'items':[self.order_dict(o) for o in items],'total':total,'page':page,'size':size,'totalPages':math.ceil(total/size) if total else 0}
    def get_order(self,db,oid):
        o=db.execute(select(Order).options(joinedload(Order.items)).where(Order.id==oid)).unique().scalar_one_or_none()
        if not o:raise HTTPException(404,'Không tìm thấy đơn hàng')
        return o
    def update_order(self,db,oid,new):
        o=self.get_order(db,oid)
        if new not in self.transitions.get(o.order_status,set()): raise HTTPException(409,'Chuyển trạng thái đơn hàng không hợp lệ')
        o.order_status=new
        if new=='COMPLETED' and o.payment_method=='COD': o.payment_status='PAID'
        db.commit(); return self.order_dict(self.get_order(db,oid))
    def update_payment(self,db,oid,new):
        o=self.get_order(db,oid)
        if o.payment_method!='COD': raise HTTPException(409,'Không thể chỉnh trạng thái thanh toán Stripe thủ công')
        if new not in {'UNPAID','PAID','REFUNDED'}: raise HTTPException(422,'Trạng thái thanh toán không hợp lệ')
        o.payment_status=new; db.commit(); return self.order_dict(self.get_order(db,oid))
