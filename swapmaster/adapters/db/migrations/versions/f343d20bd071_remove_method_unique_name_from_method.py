"""Remove method unique name from method

Revision ID: f343d20bd071
Revises: 0ed442a5f86a
Create Date: 2024-02-03 12:03:13.372640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f343d20bd071'
down_revision: Union[str, None] = '0ed442a5f86a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_commissions_value', 'commissions', type_='unique')
    op.drop_constraint('uq_methods_name', 'methods', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uq_methods_name', 'methods', ['name'])
    op.create_unique_constraint('uq_commissions_value', 'commissions', ['value'])
    # ### end Alembic commands ###
