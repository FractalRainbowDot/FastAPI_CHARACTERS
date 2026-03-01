from pydantic import BaseModel


class DamageData(BaseModel):
    id_self: int
    id_target: int

class PvEData(BaseModel):
    attacker_id: int
    npc_level: int