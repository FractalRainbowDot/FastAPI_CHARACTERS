"""Эндпоинты боев и лечения"""
from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import Annotated

from src.models.battle import DamageData, PvEData
from src.services.battle_service import BattleService
from src.services.character_service import CharacterService
from src.api.dependencies import get_battle_service, get_character_service
from src.core.exceptions import NotFoundException, BadRequestException

router = APIRouter(prefix="/battle", tags=["Battle"])


@router.post("/pvp")
async def pvp_battle(data: Annotated[DamageData, Depends()], service: BattleService = Depends(get_battle_service)):
    try:
        result = await service.pvp_battle(data.id_self, data.id_target)
        return {"log": result}
    except (NotFoundException, BadRequestException) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pve/{attacker_id}")
async def pve_battle(data: Annotated[PvEData, Depends()], service: BattleService = Depends(get_battle_service)):
    try:
        result = await service.pve_battle(data)
        return {"log": result}
    except (NotFoundException, BadRequestException) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/heal-all")
async def heal_all(service: CharacterService = Depends(get_character_service)):
    await service.heal_all()
    return {"message": "ALL HEALED"}


@router.post("/heal/{character_id}")
async def heal_one(character_id: int, service: CharacterService = Depends(get_character_service)):
    try:
        char = await service.heal_one(character_id)
        return {"message": f"Character {char.name} is healed"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
