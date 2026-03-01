from pydantic import BaseModel, ConfigDict


class NpcReadSchema(BaseModel):
    id: int
    name: str
    level: int
    current_health: float
    max_health: float
    damage: float
    armour: float

    model_config = ConfigDict(from_attributes=True)
