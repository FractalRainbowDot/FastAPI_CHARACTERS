from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.database.session import PlayerSessionDep, player_engine, npc_engine, NpcSessionDep
from app.schemas.character_schema import CharacterAddSchema, CharacterReadSchema, CharacterModel, \
    Base, DamageData, NonPlayableCharacters, NpcReadSchema, CharacterDelete
from app.battle.do_damage import do_damage
from app.battle.heal import heal_all, heal_one
from app.battle.pve_battle import fight_creep
from app.database.queries import get_character_by_id, remove_character_from_db, show_characters, add_character_to_db, \
    add_creep_to_db

router_battle = APIRouter(
    prefix='/battle',
    tags=['BATTLE'],
)

router_DB = APIRouter(
    prefix='/database',
    tags=['DATABASE'],
)


"""СОЗДАТЬ БД НПС"""
@router_DB.post('/create_DB_npc')
async def setup_db_npc():
    async with npc_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'message' : 'NPC_DATABASE created'}


"""ДРОПНУТЬ И СОЗДАТЬ БАЗУ ДАННЫХ ИГРОКОВ"""
@router_DB.post('/create_DB')
async def setup_db():
    async with player_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'message': 'players_DATABASE created'}


'''ДОБАВИТЬ ИГРОКА'''
@router_DB.post('/add_character_to_DB')
async def add_character(data: Annotated[CharacterAddSchema, Depends()], session: PlayerSessionDep):
    result = await add_character_to_db(data, session)
    return result

"""ДОБАВИТЬ КРИПА"""
@router_DB.post('/add_npc_to_DB', response_model=NpcReadSchema)
async def add_creep(data: int, session: NpcSessionDep):
    result = await add_creep_to_db(data, session)
    return result


"""УДАЛИТЬ ПЕРСОНАЖА"""
@router_DB.post('/remove_character_from_DB')
async def remove(data: Annotated[CharacterDelete, Depends()], session: PlayerSessionDep):
    result = await remove_character_from_db(data, session)
    return result


'''ВСЕ ПЕРСОНАЖИ'''
@router_DB.get('/all_characters')
async def show(session: PlayerSessionDep) -> list[CharacterReadSchema]:
    result = await show_characters(session)
    return result


'''подробный ПЕРСОНАЖ ПО АЙДИ'''
@router_DB.get('/character_info_by_id', response_model=CharacterReadSchema)
async def get_character(session: PlayerSessionDep, character_id: int):
    result = await get_character_by_id(session, character_id)
    return result


'''СРАЖЕНИЕ ДВУХ ИГРОКОВ'''
@router_battle.post('/do_hit')
async def battle(session: PlayerSessionDep, data: Annotated[DamageData, Depends()]):
    result = await do_damage(session, data)
    await session.commit()
    return result


'''ЗАЛЕЧИТЬ ВСЕХ ЧЕБУРЕКОВ'''
@router_battle.post('/heal_all')
async def heal_all_chars(session: PlayerSessionDep):
    await heal_all(session)
    return {'message': 'ALL HEALED'}


'''ЗАЛЕЧИТЬ ОДНОГО'''
@router_battle.post('/heal/{character_id}')
async def heal_one_char(character_id: int, session: PlayerSessionDep):
    character = await heal_one(session, character_id)
    return f'Character {character.name} is healed'


'''СРАЗИТЬСЯ С КРИПОМ'''
@router_battle.post('/fight_creep/{attacker_id}')
async def pve_fight_endpoint(attacker_id: int, npc_level: int, session_player: PlayerSessionDep, session_npc: NpcSessionDep):
    attacker = await session_player.get(CharacterModel, attacker_id)
    if not attacker:
        raise HTTPException(status_code=404, detail=f"Игрок с ID {attacker_id} не найден")

    result = await fight_creep(session_player, session_npc, attacker, npc_level)
    return result
