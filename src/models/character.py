from enum import StrEnum
from pydantic import BaseModel, ConfigDict


class CharacterClassChoice(StrEnum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    CLERIC = "cleric"


class CharacterAddSchema(BaseModel):
    name: str
    char_class: CharacterClassChoice


class CharacterDelete(BaseModel):
    id: int


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
        from_attributes=True,  # Позволяет Pydantic читать данные из ORM-моделей SQLAlchemy
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
