"""Эндпоинты NPC"""
from fastapi import APIRouter, Depends, HTTPException
from src.models.npc import NpcReadSchema
from src.services.npc_service import NpcService
from src.api.dependencies import get_npc_service
from src.core.exceptions import BadRequestException

router = APIRouter(prefix="/npcs", tags=["NPCs"])


@router.post("/", response_model=NpcReadSchema)
async def add_npc(level: int, service: NpcService = Depends(get_npc_service)):
    try:
        return await service.get_or_create_npc(level)
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
