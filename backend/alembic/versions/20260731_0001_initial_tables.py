"""create categories products users

Revision ID: 20260731_0001
Revises:
Create Date: 2026-07-31
"""
from alembic import op
import sqlalchemy as sa

revision = '20260731_0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('categories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('slug', sa.String(120), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint('name'), sa.UniqueConstraint('slug'))
    op.create_index('ix_categories_name', 'categories', ['name'])
    op.create_index('ix_categories_slug', 'categories', ['slug'])

    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('full_name', sa.String(120), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(500), nullable=False),
        sa.Column('phone', sa.String(30), nullable=True),
        sa.Column('role', sa.String(30), nullable=False, server_default='CUSTOMER'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint('email'))
    op.create_index('ix_users_email', 'users', ['email'])

    op.create_table('products',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('slug', sa.String(140), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('price', sa.Numeric(12, 2), nullable=False),
        sa.Column('image_url', sa.String(500), nullable=False, server_default='/images/placeholder.svg'),
        sa.Column('badge', sa.String(50), nullable=True),
        sa.Column('featured', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('is_new', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('available', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('object_position', sa.String(100), nullable=False, server_default='center'),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint('price > 0', name='ck_products_price_positive'),
        sa.UniqueConstraint('slug'))
    op.create_index('ix_products_name', 'products', ['name'])
    op.create_index('ix_products_slug', 'products', ['slug'])
    op.create_index('ix_products_category_id', 'products', ['category_id'])

def downgrade():
    op.drop_table('products')
    op.drop_table('users')
    op.drop_table('categories')
