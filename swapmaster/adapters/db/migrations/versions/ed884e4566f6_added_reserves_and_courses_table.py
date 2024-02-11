"""Added reserves and courses table

Revision ID: ed884e4566f6
Revises: 68e7b658fbfb
Create Date: 2024-02-11 13:36:16.533577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ed884e4566f6'
down_revision: Union[str, None] = '68e7b658fbfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reserves',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('size', sa.Float(), nullable=False),
    sa.Column('update_method', postgresql.ENUM('LOCAL', 'REMOTE', name='reserveupdatemethodenum'), nullable=False),
    sa.Column('method_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['method_id'], ['methods.id'], name=op.f('fk_reserves_method_id_methods'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_reserves'))
    )
    op.create_table('courses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('pair_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pair_id'], ['pairs.id'], name=op.f('fk_courses_pair_id_pairs'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_courses'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('courses')
    op.drop_table('reserves')
    op.execute("drop type reserveupdatemethodenum")
    # ### end Alembic commands ###
