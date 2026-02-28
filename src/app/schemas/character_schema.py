from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from enum import StrEnum

class Base(DeclarativeBase):
    pass


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


"""СХЕМА ДЛЯ ОТДАЧИ ДАННЫХ (READ)"""
class CharacterReadSchema(BaseModel):
    id: int
    name: str
    char_class: str
    alive: bool
    current_health: float
    max_health: float
    damage: float
    current_mana: float
    max_mana: float
    level: int
    experience: float

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Gandalf",
                "char_class": "mage",
                "alive": True,
                "current_health": 100.0,
                "max_health": 100.0,
                "damage": 10.0,
                "current_mana": 100.0,
                "max_mana": 100.0,
                "level": 1,
                "experience": 1.1,
            }
        }
    )

class NpcReadSchema(BaseModel):
    id: int
    name: str
    level: int
    current_health: float
    max_health: float
    damage: float
    armour: float

    model_config = ConfigDict(from_attributes=True)


'''НА УДАЛЕНИЕ'''
class CharacterDelete(BaseModel):
    id: int


"""НА ДОБАВЛЕНИЕ ИГРОКА"""
class CharacterClassChoice(StrEnum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    CLERIC = "cleric"

class CharacterAddSchema(BaseModel):
    name: str
    char_class: CharacterClassChoice

"""БИТВА"""
class DamageData(BaseModel):
    id_self: int
    id_target: int
