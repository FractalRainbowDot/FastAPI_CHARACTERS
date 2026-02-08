from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel
from enum import StrEnum


class Base(DeclarativeBase):
    pass


class CharacterModel(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    char_class: Mapped[str]
    health: Mapped[int] = mapped_column(default=100)
    alive: Mapped[bool] = mapped_column(default=True)
    damage: Mapped[int] = mapped_column(default=10)
    armour: Mapped[int] = mapped_column(default=0)


class CharacterClassChoice(StrEnum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    CLERIC = "cleric"


class CharacterAddShema(BaseModel):
    name: str
    char_class: CharacterClassChoice


class Battle(BaseModel):
    id_self: str
    id_target: str

jopass = CharacterModel(
    name='Jopass',
    char_class=CharacterClassChoice.WARRIOR
)
print(jopass.char_class)