from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from Shemas.CharacterShema import Base, CharacterAddShema, CharacterModel

app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///database/characters.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.post('/create_DB', tags=['DATABASE'])
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'message': 'ZAEBIS'}


@app.post('/add_character_to_DB', tags=['DATABASE'])
async def add_character_to_db(
        data: Annotated[CharacterAddShema, Depends()],
        session: SessionDep
):
    new_character = CharacterModel(
        name=data.name,
        char_class=data.char_class
    )
    session.add(new_character)
    await session.commit()
    return {'message': 'ZAEBIS'}


@app.get('/all_characters', tags=['DATABASE'])
async def show_characters(session: SessionDep):
    query = select(CharacterModel)
    result = await session.execute(query)
    return result.scalars().all()


@app.get('/character_info_by_id', tags=['DATABASE'])
async def get_character(session: SessionDep, character_id: int):
    query = select(CharacterModel).where(CharacterModel.id == character_id)
    result = await session.execute(query)
    return result.scalars().first()

# if __name__ == '__main__':
#     uvicorn.run("main:app", reload=True)
