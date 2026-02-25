from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel, Field, ConfigDict
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
    mana: Mapped[int] = mapped_column(default=100, server_default="100")


"""СХЕМА ДЛЯ ОТДАЧИ ДАННЫХ (READ)"""
class CharacterReadSchema(BaseModel):
    id: int
    name: str
    char_class: str
    alive: bool
    health: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Gandalf",
                "char_class": "mage",
                "alive": True,
                "health": 100
            }
        }
    )


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

'''ДЛЯ СОВЕРШЕНИЯ НАСИЛИЯ'''
class Battle(BaseModel):
    id_self: int = Field(gt=0)
    id_target: int = Field(gt=0)
