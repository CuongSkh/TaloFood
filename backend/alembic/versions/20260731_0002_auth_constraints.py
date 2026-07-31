"""normalize users for authentication and role authorization

Revision ID: 20260731_0002
Revises: 20260731_0001
Create Date: 2026-07-31
"""
from alembic import op
import sqlalchemy as sa

revision = '20260731_0002'
down_revision = '20260731_0001'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("UPDATE users SET email = lower(trim(email))")
    op.execute("UPDATE users SET role = 'CUSTOMER' WHERE role NOT IN ('CUSTOMER', 'ADMIN')")
    op.create_check_constraint('ck_users_role_valid', 'users', "role IN ('CUSTOMER', 'ADMIN')")
    op.create_index('ix_users_role', 'users', ['role'])
    op.create_index('ix_users_is_active', 'users', ['is_active'])


def downgrade():
    op.drop_index('ix_users_is_active', table_name='users')
    op.drop_index('ix_users_role', table_name='users')
    op.drop_constraint('ck_users_role_valid', 'users', type_='check')
