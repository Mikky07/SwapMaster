"""Refactored courses relationship with pair

Revision ID: a319eb571da8
Revises: 7f83f906139e
Create Date: 2024-02-22 17:04:59.354537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a319eb571da8'
down_revision: Union[str, None] = '7f83f906139e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('courses', 'update_method',
               existing_type=postgresql.ENUM('LOCAL', 'REMOTE', name='courseupdatemethodenum'),
               nullable=False)
    op.drop_constraint('fk_courses_pair_id_pairs', 'courses', type_='foreignkey')
    op.drop_column('courses', 'pair_id')
    op.add_column('pairs', sa.Column('course_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_pairs_course_id_courses'), 'pairs', 'courses', ['course_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_pairs_course_id_courses'), 'pairs', type_='foreignkey')
    op.drop_column('pairs', 'course_id')
    op.add_column('courses', sa.Column('pair_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('fk_courses_pair_id_pairs', 'courses', 'pairs', ['pair_id'], ['id'], ondelete='CASCADE')
    op.alter_column('courses', 'update_method',
               existing_type=postgresql.ENUM('LOCAL', 'REMOTE', name='courseupdatemethodenum'),
               nullable=True)
    # ### end Alembic commands ###
