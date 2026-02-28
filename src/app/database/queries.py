from fastapi import HTTPException
from sqlalchemy import func, select, delete

from app.schemas.character_schema import CharacterModel


async def hello_count_players(session):
    query = func.count(CharacterModel.id)
    result = await session.execute(query)
    return result.scalar()


async def bye_count_players(session):
    query = select(func.count(CharacterModel.id)).where(CharacterModel.alive == 1)
    result = await session.execute(query)
    return result.scalar()


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
    base_armour, base_damage = 0, 10

    if data.char_class == 'warrior':
        base_armour = 5
    elif data.char_class == 'cleric':
        base_damage = 5

    new_character = CharacterModel(
        name=data.name,
        char_class=data.char_class,
        armour=base_armour,
        damage=base_damage
    )
    session.add(new_character)
    await session.commit()
    return {'message': f'Персонажу присвоен ID {new_character.id}'}
