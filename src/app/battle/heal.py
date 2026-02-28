from sqlalchemy import update, select
from fastapi import HTTPException

from app.schemas.character_schema import CharacterModel


async def heal_all(session):
    """Восстанавливает здоровье и ману всем персонажам."""
    query = update(CharacterModel).values(
        current_health=CharacterModel.max_health,
        current_mana=CharacterModel.max_mana,
        alive=True
    )
    await session.execute(query)
    await session.commit()

async def heal_one(session, character_id: int):
    """Восстанавливает здоровье и ману одному персонажу."""
    character = await session.get(CharacterModel, character_id)
    if not character:
        raise HTTPException(status_code=404, detail=f"Персонаж с ID {character_id} не найден")
    
    character.current_health = character.max_health
    character.current_mana = character.max_mana
    character.alive = True
    
    await session.commit()
    return character
