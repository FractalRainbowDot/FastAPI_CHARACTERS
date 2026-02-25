"""update_warrior_armour and cleric_damage

Revision ID: 1e9ce54fa737
Revises: 35a38a75934c
Create Date: 2026-02-25 09:58:01.174975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e9ce54fa737'
down_revision: Union[str, Sequence[str], None] = '35a38a75934c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Обновляем броню всем старым воинам
    op.execute("UPDATE characters SET armour = 5 WHERE char_class = 'warrior'")
    op.execute("UPDATE characters SET damage = 5 WHERE char_class = 'cleric'")


def downgrade() -> None:
    # Если откатываем миграцию - забираем броню обратно (по желанию)
    op.execute("UPDATE characters SET armour = 0 WHERE char_class = 'warrior'")
    op.execute("UPDATE characters SET damage = 10 WHERE char_class = 'cleric'")