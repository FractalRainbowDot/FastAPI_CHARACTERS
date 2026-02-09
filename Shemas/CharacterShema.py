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
    # cock_size: Mapped[int] = mapped_column(default=2)


class CharacterShow(BaseModel):
    id: int
    name: str
    char_class: str
    health: int
    alive: bool
    damage: int
    armour: int

'''НА УДАЛЕНИЕ'''
class CharacterDelete(BaseModel):
    id: int


"""НА ДОБАВЛЕНИЕ ИГРОКА"""
class CharacterAddShema(BaseModel):
    name: str
    char_class: CharacterClassChoice

class CharacterClassChoice(StrEnum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    CLERIC = "cleric"


'''ДЛЯ СОВЕРШЕНИЯ НАСИЛИЯ'''
class Battle(BaseModel):
    id_self: str
    id_target: str
