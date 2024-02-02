"""Added pairs table

Revision ID: 71d0a7ac2c6e
Revises: 071d731216eb
Create Date: 2024-02-02 14:03:45.205772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71d0a7ac2c6e'
down_revision: Union[str, None] = '071d731216eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pairs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('method_from_id', sa.Integer(), nullable=True),
    sa.Column('method_to_id', sa.Integer(), nullable=True),
    sa.Column('commission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['commission_id'], ['commissions.id'], name=op.f('fk_pairs_commission_id_commissions')),
    sa.ForeignKeyConstraint(['method_from_id'], ['methods.id'], name=op.f('fk_pairs_method_from_id_methods'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['method_to_id'], ['methods.id'], name=op.f('fk_pairs_method_to_id_methods'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_pairs'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pairs')
    # ### end Alembic commands ###
