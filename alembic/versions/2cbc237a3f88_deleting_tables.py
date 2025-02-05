"""deleting tables

Revision ID: 2cbc237a3f88
Revises: 77325592d7e0
Create Date: 2025-02-04 17:07:25.546095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cbc237a3f88'
down_revision: Union[str, None] = '77325592d7e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_choices_id'), table_name='choices')
    op.drop_table('choices')
    op.drop_index(op.f('ix_questions_id'), table_name='questions')
    op.drop_table('questions')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_quizzes_title'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_subject'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_id'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_genre'), table_name='quizzes')
    op.drop_table('quizzes')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
