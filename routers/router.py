from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from Schemas.CharacterSchema import CharacterAddSchema, CharacterDelete, CharacterReadSchema, CharacterModel, \
    Base, DamageData
from battle.do_damage import do_damage
from battle.heal_all import heal_all
from battle.pve_battle import fight_creep
from database.queries import get_character_by_id, remove_character_from_db, show_characters, add_character_to_db

engine = create_async_engine('sqlite+aiosqlite:///database/characters.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

router_battle = APIRouter(
    prefix='/battle',
    tags=['BATTLE'],
)

router_DB = APIRouter(
    prefix='/database',
    tags=['DATABASE'],
)

"""ДРОПНУТЬ И СОЗДАТЬ БАЗУ ДАННЫХ"""
@router_DB.post('/create_DB')
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'message': 'ZAEBIS'}


'''ДОБАВИТЬ ИГРОКА'''
@router_DB.post('/add_character_to_DB')
async def add_character(data: Annotated[CharacterAddSchema, Depends()], session: SessionDep):
    result = await add_character_to_db(data, session)
    return result


"""УДАЛИТЬ ПЕРСОНАЖА"""
@router_DB.post('/remove_character_from_DB')
async def remove(data: Annotated[CharacterDelete, Depends()], session: SessionDep):
    result = await remove_character_from_db(data, session)
    return result


'''ВСЕ ПЕРСОНАЖИ'''
@router_DB.get('/all_characters')
async def show(session: SessionDep) -> list[CharacterReadSchema]:
    result = await show_characters(session)
    return result


'''подробный ПЕРСОНАЖ ПО АЙДИ'''
@router_DB.get('/character_info_by_id')
async def get_character(session: SessionDep, character_id: int):
    result = await get_character_by_id(session, character_id)
    return result


'''СРАЖЕНИЕ ДВУХ ИГРОКОВ'''
@router_battle.post('/do_hit')
async def battle(session: SessionDep, data: DamageData):
    result = await do_damage(session, data)
    await session.commit() # Завершаем транзакцию здесь
    return result


'''ЗАЛЕЧИТЬ ВСЕХ ЧЕБУРЕКОВ'''
@router_battle.post('/heal_all')
async def heal_all_chars(session: SessionDep):
    await heal_all(session)
    return {'message': 'ALL HEALED'}


'''СРАЗИТЬСЯ С КРИПОМ'''
@router_battle.post('/fight_creep/{attacker_id}')
async def pve_fight_endpoint(attacker_id: int, session: SessionDep):
    attacker = await session.get(CharacterModel, attacker_id)
    if not attacker:
        raise HTTPException(status_code=404, detail=f"Игрок с ID {attacker_id} не найден")

    result = await fight_creep(session, attacker_id)
    return result
