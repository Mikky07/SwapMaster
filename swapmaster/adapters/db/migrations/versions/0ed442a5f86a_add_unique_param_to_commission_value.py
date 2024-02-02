"""Add unique param to commission value

Revision ID: 0ed442a5f86a
Revises: 71d0a7ac2c6e
Create Date: 2024-02-02 21:14:10.809882

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ed442a5f86a'
down_revision: Union[str, None] = '71d0a7ac2c6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f('uq_commissions_value'), 'commissions', ['value'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_commissions_value'), 'commissions', type_='unique')
    # ### end Alembic commands ###