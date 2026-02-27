"""rename health to hp

Revision ID: 48cf8037ed04
Revises: 5e8019f76e83
Create Date: 2026-02-27 09:42:48.481116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48cf8037ed04'
down_revision: Union[str, Sequence[str], None] = '5e8019f76e83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Используем batch_alter_table для безопасной работы со SQLite
    with op.batch_alter_table('characters') as batch_op:
        batch_op.alter_column('health', new_column_name='current_health')


def downgrade() -> None:
    # Обратное переименование для возможности отката миграции
    with op.batch_alter_table('characters') as batch_op:
        batch_op.alter_column('current_health', new_column_name='health')
