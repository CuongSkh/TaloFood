"""payments and stripe support
Revision ID: 20260731_0004
Revises: 20260731_0003
"""
from alembic import op
import sqlalchemy as sa
revision='20260731_0004'; down_revision='20260731_0003'; branch_labels=None; depends_on=None
def upgrade():
    op.create_table('payments',
      sa.Column('id',sa.Integer(),primary_key=True),sa.Column('order_id',sa.Integer(),sa.ForeignKey('orders.id',ondelete='CASCADE'),nullable=False),sa.Column('provider',sa.String(20),nullable=False),sa.Column('provider_session_id',sa.String(255),nullable=True),sa.Column('transaction_id',sa.String(255),nullable=True),sa.Column('amount',sa.Numeric(14,2),nullable=False),sa.Column('currency',sa.String(10),nullable=False),sa.Column('status',sa.String(20),nullable=False),sa.Column('checkout_url',sa.Text(),nullable=True),sa.Column('failure_reason',sa.Text(),nullable=True),sa.Column('paid_at',sa.DateTime(timezone=True),nullable=True),sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False),sa.Column('updated_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False),sa.CheckConstraint("provider IN ('STRIPE')",name='ck_payments_provider'),sa.CheckConstraint("status IN ('PENDING','SUCCEEDED','FAILED','CANCELED','REFUNDED')",name='ck_payments_status'),sa.CheckConstraint('amount > 0',name='ck_payments_amount_positive'))
    op.create_index('ix_payments_order_id','payments',['order_id']);op.create_index('ix_payments_status','payments',['status']);op.create_index('ix_payments_created_at','payments',['created_at']);op.create_index('ix_payments_provider_session_id','payments',['provider_session_id'],unique=True);op.create_index('ix_payments_transaction_id','payments',['transaction_id'],unique=True)
def downgrade(): op.drop_table('payments')
