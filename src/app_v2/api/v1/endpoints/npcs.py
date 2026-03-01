"""Эндпоинты NPC"""
from fastapi import APIRouter, Depends, HTTPException
from app_v2.models.npc import NpcReadSchema
from app_v2.services.npc_service import NpcService
from app_v2.api.dependencies import get_npc_service

router = APIRouter(prefix="/npcs", tags=["NPCs"])


@router.post("/", response_model=NpcReadSchema)
async def add_npc(level: int, service: NpcService = Depends(get_npc_service)):
    try:
        return await service.get_or_create_npc(level)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
