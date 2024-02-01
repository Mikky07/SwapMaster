"""Added method table

Revision ID: 13b249ba2743
Revises: 5503c0e18067
Create Date: 2024-02-01 17:58:16.276359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13b249ba2743'
down_revision: Union[str, None] = '5503c0e18067'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('methods',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], name=op.f('fk_methods_currency_id_currencies'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_methods')),
    sa.UniqueConstraint('name', name=op.f('uq_methods_name'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('methods')
    # ### end Alembic commands ###
