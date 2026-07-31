from datetime import datetime
from decimal import Decimal
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Payment(Base):
    __tablename__='payments'
    __table_args__=(
        CheckConstraint("provider IN ('STRIPE')", name='ck_payments_provider'),
        CheckConstraint("status IN ('PENDING','SUCCEEDED','FAILED','CANCELED','REFUNDED')", name='ck_payments_status'),
        CheckConstraint('amount > 0', name='ck_payments_amount_positive'),
    )
    id: Mapped[int]=mapped_column(primary_key=True)
    order_id: Mapped[int]=mapped_column(ForeignKey('orders.id',ondelete='CASCADE'),index=True,nullable=False)
    provider: Mapped[str]=mapped_column(String(20),nullable=False,default='STRIPE')
    provider_session_id: Mapped[str|None]=mapped_column(String(255),unique=True,index=True,nullable=True)
    transaction_id: Mapped[str|None]=mapped_column(String(255),unique=True,index=True,nullable=True)
    amount: Mapped[Decimal]=mapped_column(Numeric(14,2),nullable=False)
    currency: Mapped[str]=mapped_column(String(10),nullable=False,default='vnd')
    status: Mapped[str]=mapped_column(String(20),nullable=False,default='PENDING',index=True)
    checkout_url: Mapped[str|None]=mapped_column(Text,nullable=True)
    failure_reason: Mapped[str|None]=mapped_column(Text,nullable=True)
    paid_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),index=True)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    order=relationship('Order',back_populates='payments')
