from sqlalchemy import func, select

from Shemas.CharacterShema import CharacterModel



async def hello_count_players(session):
    query = func.count(CharacterModel.id)
    result = await session.execute(query)
    return result.scalar()

async def bye_count_players(session):
    query = select(func.count(CharacterModel.id)).where(CharacterModel.alive == 1)
    result = await session.execute(query)
    return result.scalar()