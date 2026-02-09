from sqlalchemy import update

from Shemas.CharacterShema import CharacterModel


async def heal_all(session):
    query = update(CharacterModel).values(health=100, alive=True)
    await session.execute(query)
    await session.commit()
