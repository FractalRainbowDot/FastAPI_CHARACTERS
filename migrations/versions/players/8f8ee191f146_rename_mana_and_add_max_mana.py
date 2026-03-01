"""rename mana and add max_mana

Revision ID: 8f8ee191f146
Revises: 48cf8037ed04
Create Date: 2026-02-27 10:50:36.160033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f8ee191f146'
down_revision: Union[str, Sequence[str], None] = '48cf8037ed04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('characters') as batch_op:
        batch_op.alter_column('mana', new_column_name='current_mana')
        batch_op.add_column(sa.Column('max_mana', sa.Integer(), server_default='100', nullable=False))

def downgrade() -> None:
    with op.batch_alter_table('characters') as batch_op:
        batch_op.drop_column('max_mana')
        batch_op.alter_column('current_mana', new_column_name='mana')
