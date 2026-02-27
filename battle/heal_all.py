from sqlalchemy import update

from Schemas.CharacterSchema import CharacterModel


async def heal_all(session):
    query = update(CharacterModel).values(
        current_health=CharacterModel.max_health,
        current_mana=CharacterModel.max_mana,
        alive=True
    )
    await session.execute(query)
    await session.commit()
