from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class NonPlayableCharacters(Base):
    __tablename__ = "NonPlayableCharacters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default="Ogre")
    char_class: Mapped[str] = mapped_column(default="monster")
    current_health: Mapped[float] = mapped_column(default=100)
    max_health: Mapped[float] = mapped_column(default=100)
    alive: Mapped[bool] = mapped_column(default=True)
    damage: Mapped[float] = mapped_column(default=10)
    armour: Mapped[float] = mapped_column(default=0)
    level: Mapped[int] = mapped_column(default=1)
    exp_reward: Mapped[float] = mapped_column(default=1)
