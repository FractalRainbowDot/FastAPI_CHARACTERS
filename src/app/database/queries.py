from fastapi import HTTPException
from sqlalchemy import func, select, delete, update

from app.schemas.character_schema import CharacterModel, NonPlayableCharacters, CharacterReadSchema


async def hello_count_players(session):
    query = func.count(CharacterModel.id)
    result = await session.execute(query)
    return result.scalar()

async def bye_count_players(session):
    query = select(func.count(CharacterModel.id)).where(CharacterModel.alive == 1)
    result = await session.execute(query)
    return result.scalar()

async def get_npc_by_lvl(session, npc_level) -> NonPlayableCharacters:
    if npc_level < 1:
        raise HTTPException(status_code=400, detail='Неправильный ввод')
    query = select(NonPlayableCharacters).where(NonPlayableCharacters.level == npc_level)
    result = await session.execute(query)
    return result.scalars().first()

async def get_character_by_id(session, character_id):
    if character_id <= 0:
        raise HTTPException(status_code=400, detail='Неправильный ввод')
    query = select(CharacterModel).where(CharacterModel.id == character_id)
    result = await session.execute(query)
    return result.scalars().first()


async def remove_character_from_db(data, session):
    query = delete(CharacterModel).where(CharacterModel.id == data.id)
    result = await session.execute(query)
    await session.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail='Такого персонажа нет')
    else:
        return f'Пользователь с ID {data.id} удалён'


async def show_characters(session):
    query = select(CharacterModel).order_by(CharacterModel.id)
    result = await session.execute(query)
    return result.scalars().all()


async def add_character_to_db(data, session):
    base_armour, base_damage = 1, 10

    if data.char_class == 'warrior':
        base_armour += 5
        base_damage -= 3
    elif data.char_class == 'cleric':
        base_damage -= 5

    new_character = CharacterModel(
        name=data.name,
        char_class=data.char_class,
        armour=base_armour,
        damage=base_damage
    )
    session.add(new_character)
    await session.commit()
    return {'message': f'Персонажу {new_character.name} присвоен ID {new_character.id}'}


async def add_creep_to_db(data, session) -> NonPlayableCharacters:
    if data is None or data < 1:
        raise HTTPException(status_code=400, detail='Неправильный ввод')
    cr_level = data
    cr_health = 50 * ((1 + 0.1) ** (cr_level - 1))
    cr_dmg = 4 + 1 * (cr_level ** 1.2)
    cr_armour = 2 * (cr_level ** 1.1)
    exp_reward = 10 * (cr_level ** 2)

    ogre = NonPlayableCharacters(
        level=cr_level,
        max_health=cr_health,
        damage=cr_dmg,
        armour=cr_armour,
        current_health=cr_health,
        exp_reward=exp_reward
    )

    session.add(ogre)
    await session.flush()
    await session.refresh(ogre)
    await session.commit()
    return ogre

async def update_npc_stats(session, npc: NonPlayableCharacters):
    """Обновляет статы NPC в базе данных."""
    query = (
        update(NonPlayableCharacters)
        .where(NonPlayableCharacters.id == npc.id)
        .values(current_health=npc.current_health)
    )
    await session.execute(query)
    await session.commit()
