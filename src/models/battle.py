from pydantic import BaseModel


class DamageData(BaseModel):
    id_self: int
    id_target: int
