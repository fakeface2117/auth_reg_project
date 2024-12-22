"""change orders

Revision ID: 8e423e51d080
Revises: b7d722bd8a35
Create Date: 2024-12-22 22:04:48.843652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e423e51d080'
down_revision: Union[str, None] = 'b7d722bd8a35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('store_orders', sa.Column('total_price', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('store_orders', 'total_price')
    # ### end Alembic commands ###