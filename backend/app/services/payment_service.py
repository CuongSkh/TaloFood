import math
from datetime import datetime,timezone
from decimal import Decimal
import stripe
from fastapi import HTTPException
from sqlalchemy import func,select
from sqlalchemy.orm import Session,joinedload
from app.core.config import STRIPE_SECRET_KEY,STRIPE_WEBHOOK_SECRET,STRIPE_SUCCESS_URL,STRIPE_CANCEL_URL,STRIPE_CURRENCY
from app.models.order import Order
from app.models.payment import Payment

class PaymentService:
    def _ensure(self):
        if not STRIPE_SECRET_KEY: raise HTTPException(503,'Stripe chưa được cấu hình. COD vẫn hoạt động bình thường.')
        stripe.api_key=STRIPE_SECRET_KEY
    def _resp(self,p):
        return {'id':p.id,'order_id':p.order_id,'provider':p.provider,'provider_session_id':p.provider_session_id,'transaction_id':p.transaction_id,'amount':float(p.amount),'currency':p.currency,'status':p.status,'checkout_url':p.checkout_url,'failure_reason':p.failure_reason,'paid_at':p.paid_at,'created_at':p.created_at,'updated_at':p.updated_at}
    def create_session(self,db,user,order_id):
        self._ensure(); order=db.get(Order,order_id)
        if not order: raise HTTPException(404,'Không tìm thấy đơn hàng')
        if order.user_id!=user.id and user.role!='ADMIN': raise HTTPException(403,'Bạn không có quyền thanh toán đơn hàng này')
        if order.order_status=='CANCELLED': raise HTTPException(409,'Đơn hàng đã bị hủy')
        if order.payment_status=='PAID': raise HTTPException(409,'Đơn hàng đã được thanh toán')
        if order.payment_method!='STRIPE': raise HTTPException(409,'Đơn hàng này không sử dụng Stripe')
        pending=db.scalar(select(Payment).where(Payment.order_id==order.id,Payment.status=='PENDING').order_by(Payment.id.desc()))
        payment=pending or Payment(order_id=order.id,provider='STRIPE',amount=order.total_amount,currency=STRIPE_CURRENCY,status='PENDING')
        if not pending: db.add(payment); db.flush()
        amount=int(Decimal(order.total_amount))
        try:
            session=stripe.checkout.Session.create(
                mode='payment',
                line_items=[{'price_data':{'currency':STRIPE_CURRENCY,'product_data':{'name':f'TaloFood - Đơn hàng {order.order_code}'},'unit_amount':amount},'quantity':1}],
                success_url=f'{STRIPE_SUCCESS_URL}?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=f'{STRIPE_CANCEL_URL}?order_id={order.id}',
                metadata={'order_id':str(order.id),'order_code':order.order_code,'user_id':str(order.user_id),'payment_id':str(payment.id)},
            )
            payment.provider_session_id=session.id; payment.checkout_url=session.url; order.payment_status='PENDING'; db.commit()
            return {'payment_id':payment.id,'session_id':session.id,'checkout_url':session.url}
        except Exception as exc:
            db.rollback(); raise HTTPException(502,f'Không thể tạo phiên Stripe: {str(exc)}')
    def verify(self,db,user,session_id):
        self._ensure()
        try: session=stripe.checkout.Session.retrieve(session_id)
        except Exception: raise HTTPException(400,'Stripe session không hợp lệ')
        payment=db.scalar(select(Payment).where(Payment.provider_session_id==session_id))
        if not payment: raise HTTPException(404,'Không tìm thấy giao dịch thanh toán')
        order=db.get(Order,payment.order_id)
        if order.user_id!=user.id and user.role!='ADMIN': raise HTTPException(403,'Bạn không có quyền xác minh giao dịch này')
        if payment.status=='SUCCEEDED': return {'payment_id':payment.id,'order_id':order.id,'order_code':order.order_code,'amount':float(payment.amount),'currency':payment.currency,'payment_status':payment.status,'order_payment_status':order.payment_status}
        metadata=session.get('metadata') or {}
        valid=(session.get('payment_status')=='paid' and int(session.get('amount_total') or 0)==int(Decimal(order.total_amount)) and str(session.get('currency','')).lower()==STRIPE_CURRENCY.lower() and str(metadata.get('order_id'))==str(order.id) and str(metadata.get('payment_id'))==str(payment.id))
        if not valid:
            payment.status='FAILED'; payment.failure_reason='Stripe verification mismatch'; order.payment_status='FAILED'; db.commit(); raise HTTPException(409,'Không thể xác minh thanh toán Stripe')
        payment.status='SUCCEEDED'; payment.transaction_id=str(session.get('payment_intent') or session.id); payment.paid_at=datetime.now(timezone.utc); payment.failure_reason=None; order.payment_status='PAID'; db.commit()
        return {'payment_id':payment.id,'order_id':order.id,'order_code':order.order_code,'amount':float(payment.amount),'currency':payment.currency,'payment_status':payment.status,'order_payment_status':order.payment_status}
    def webhook(self,db,payload,signature):
        if not STRIPE_WEBHOOK_SECRET: raise HTTPException(503,'STRIPE_WEBHOOK_SECRET chưa được cấu hình')
        try: event=stripe.Webhook.construct_event(payload,signature,STRIPE_WEBHOOK_SECRET)
        except Exception: raise HTTPException(400,'Webhook signature không hợp lệ')
        if event['type']=='checkout.session.completed':
            session=event['data']['object']; payment=db.scalar(select(Payment).where(Payment.provider_session_id==session['id']))
            if payment and payment.status!='SUCCEEDED':
                order=db.get(Order,payment.order_id)
                if session.get('payment_status')=='paid' and int(session.get('amount_total') or 0)==int(Decimal(order.total_amount)):
                    payment.status='SUCCEEDED'; payment.transaction_id=str(session.get('payment_intent') or session['id']); payment.paid_at=datetime.now(timezone.utc); order.payment_status='PAID'; db.commit()
        return {'received':True}

    def cancel_checkout(self,db,user,order_id):
        order=db.get(Order,order_id)
        if not order: raise HTTPException(404,'Không tìm thấy đơn hàng')
        if order.user_id!=user.id and user.role!='ADMIN': raise HTTPException(403,'Bạn không có quyền cập nhật thanh toán này')
        payment=db.scalar(select(Payment).where(Payment.order_id==order_id,Payment.status=='PENDING').order_by(Payment.id.desc()))
        if payment:
            payment.status='CANCELED'; payment.failure_reason='Khách hàng hủy Stripe Checkout'
        if order.payment_status!='PAID': order.payment_status='FAILED'
        db.commit(); return {'message':'Đã ghi nhận Stripe Checkout bị hủy','order_id':order.id}

    def by_order(self,db,user,order_id):
        order=db.get(Order,order_id)
        if not order: raise HTTPException(404,'Không tìm thấy đơn hàng')
        if order.user_id!=user.id and user.role!='ADMIN': raise HTTPException(403,'Bạn không có quyền xem thanh toán này')
        return [self._resp(x) for x in db.scalars(select(Payment).where(Payment.order_id==order_id).order_by(Payment.created_at.desc())).all()]
    def admin_list(self,db,page,size,provider=None,status=None,order_code=None):
        q=select(Payment).join(Payment.order)
        if provider:q=q.where(Payment.provider==provider)
        if status:q=q.where(Payment.status==status)
        if order_code:q=q.where(Order.order_code.ilike(f'%{order_code}%'))
        total=db.scalar(select(func.count()).select_from(q.subquery())) or 0
        items=db.scalars(q.order_by(Payment.created_at.desc()).offset((page-1)*size).limit(size)).all()
        return {'items':[self._resp(x) for x in items],'total':total,'page':page,'size':size,'totalPages':math.ceil(total/size) if total else 0}
