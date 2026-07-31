from datetime import datetime
from decimal import Decimal
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        CheckConstraint("payment_method IN ('COD','STRIPE','PAYPAL','VNPAY')", name='ck_orders_payment_method'),
        CheckConstraint("payment_status IN ('UNPAID','PENDING','PAID','FAILED','REFUNDED')", name='ck_orders_payment_status'),
        CheckConstraint("order_status IN ('PENDING','CONFIRMED','PREPARING','DELIVERING','COMPLETED','CANCELLED')", name='ck_orders_order_status'),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    order_code: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='RESTRICT'), index=True, nullable=False)
    receiver_name: Mapped[str] = mapped_column(String(120), nullable=False)
    receiver_phone: Mapped[str] = mapped_column(String(30), nullable=False)
    delivery_address: Mapped[str] = mapped_column(String(500), nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    delivery_fee: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False, default=0)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(20), nullable=False, default='COD')
    payment_status: Mapped[str] = mapped_column(String(20), nullable=False, default='UNPAID')
    order_status: Mapped[str] = mapped_column(String(20), nullable=False, default='PENDING', index=True)
    cancel_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

class OrderItem(Base):
    __tablename__ = 'order_items'
    __table_args__ = (CheckConstraint('quantity > 0', name='ck_order_items_quantity_positive'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), index=True, nullable=False)
    product_id: Mapped[int | None] = mapped_column(ForeignKey('products.id', ondelete='SET NULL'), nullable=True)
    product_name: Mapped[str] = mapped_column(String(120), nullable=False)
    product_image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    line_total: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    order = relationship('Order', back_populates='items')
