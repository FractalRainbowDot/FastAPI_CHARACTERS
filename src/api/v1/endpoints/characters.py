"""Эндпоинты игроков"""
from fastapi import APIRouter, Depends, HTTPException
from src.models.character import CharacterAddSchema, CharacterReadSchema, CharacterDelete
from src.services.character_service import CharacterService
from src.api.dependencies import get_character_service

router = APIRouter(prefix="/characters", tags=["Characters"])


@router.post("/", response_model=CharacterReadSchema)
async def add_character(data: CharacterAddSchema, service: CharacterService = Depends(get_character_service)):
    return await service.create_character(data)


@router.get("/", response_model=list[CharacterReadSchema])
async def get_all_characters(service: CharacterService = Depends(get_character_service)):
    # Просто дергаем репозиторий через сервис
    return await service.repo.get_all()


@router.get("/{character_id}", response_model=CharacterReadSchema)
async def get_character(character_id: int, service: CharacterService = Depends(get_character_service)):
    char = await service.repo.get_by_id(character_id)
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    return char


@router.delete("/")
async def delete_character(data: CharacterDelete, service: CharacterService = Depends(get_character_service)):
    try:
        result = await service.delete_character(data.id)
        return {"message": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
