from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class CharacterModel(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    char_class: Mapped[str]
    current_health: Mapped[float] = mapped_column(default=100)
    max_health: Mapped[float] = mapped_column(default=100, server_default="100")
    alive: Mapped[bool] = mapped_column(default=True)
    damage: Mapped[float] = mapped_column(default=10)
    armour: Mapped[float] = mapped_column(default=0)
    current_mana: Mapped[float] = mapped_column(default=100, server_default="100")
    max_mana: Mapped[float] = mapped_column(default=100, server_default="100")
    level: Mapped[int] = mapped_column(default=1, server_default="1")
    experience: Mapped[float] = mapped_column(default=0, server_default="0")
