"""Эндпоинты игроков"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from src.models.character import CharacterAddSchema, CharacterReadSchema, CharacterDelete
from src.services.character_service import CharacterService
from src.api.dependencies import get_character_service
from src.core.exceptions import NotFoundException

router = APIRouter(prefix="/characters", tags=["Characters"])


@router.post("/", response_model=CharacterReadSchema)
async def add_character(data: Annotated[CharacterAddSchema, Depends()], service: CharacterService = Depends(get_character_service)):
    return await service.create_character(data)


@router.get("/", response_model=list[CharacterReadSchema])
async def get_all_characters(service: CharacterService = Depends(get_character_service)):
    # Просто дергаем репозиторий через сервис
    return await service.repo.get_all()


@router.get("/{character_id}", response_model=CharacterReadSchema)
async def get_character(character_id: int, service: CharacterService = Depends(get_character_service)):
    try:
        char = await service.repo.get_by_id(character_id)
        if not char:
            raise NotFoundException("Персонаж")
        return char
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/")
async def delete_character(data: Annotated[CharacterDelete, Depends()], service: CharacterService = Depends(get_character_service)):
    try:
        result = await service.delete_character(data.id)
        return {"message": result}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
