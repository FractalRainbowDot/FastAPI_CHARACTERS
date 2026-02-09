from sqlalchemy import update

from Shemas.CharacterShema import CharacterModel


async def heal_all(session):
    query = update(CharacterModel).values(health=100)
    await session.execute(query)
    query_alive = update(CharacterModel).values(alive=True)
    await session.execute(query_alive)
    await session.commit()
