"""init db

Revision ID: e51a2d162290
Revises: 
Create Date: 2024-11-10 23:21:18.392835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e51a2d162290'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    roles_table = op.create_table('roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role', sa.Enum('USER', 'SELLER', 'ADMIN', name='roleenum'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('store_products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('brand', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('counts', sa.JSON(), nullable=True),
    sa.Column('parameters', sa.JSON(), nullable=True),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Uuid(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('registered_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('sex', sa.Enum('MAN', 'WOMAN', name='sexenum'), nullable=False),
    sa.Column('contacts', sa.JSON(), nullable=True),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('store_bucket',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('added_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['store_products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('store_orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('order_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('order_status', sa.Enum('CREATED', 'IS_GOING_TO', 'IN_DELIVERY', 'DELIVERED', 'PRESENTED', 'CANCELED', name='orderstatusenum'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('store_order_products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(), nullable=False),
    sa.Column('product_price', sa.Integer(), nullable=False),
    sa.Column('product_count', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['store_orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['store_products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.bulk_insert(
        roles_table,
        [
            {'id': 1, 'role': 'USER'},
            {'id': 2, 'role': 'SELLER'},
            {'id': 3, 'role': 'ADMIN'},
        ]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('store_order_products')
    op.drop_table('store_orders')
    op.drop_table('store_bucket')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('store_products')
    op.drop_table('roles')
    # ### end Alembic commands ###