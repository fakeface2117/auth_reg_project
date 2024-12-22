"""add column sum_counts to Products

Revision ID: 83e2d7b73c87
Revises: 90d1888876a4
Create Date: 2024-11-23 19:34:27.546971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83e2d7b73c87'
down_revision: Union[str, None] = '90d1888876a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('store_products', sa.Column('sum_count', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('store_products', 'sum_count')
    # ### end Alembic commands ###