from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from uvicorn import lifespan

from Shemas.CharacterShema import Base, CharacterAddShema, CharacterModel, Battle
from battle.do_damage import do_damage
from battle.heal_all import heal_all
from database.hello_count import hello_count_players, bye_count_players


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f'{'Запуск приложения':-^100}')
    async with new_session() as session:
        count = await hello_count_players(session)
        print(f'К бою готовы {count} игроков')
    yield
    print(f'{'Выключение':-^100}')
    async with new_session() as session:
        count = await bye_count_players(session)
        print(f'В живых осталось {count} игроков')

app = FastAPI(lifespan=lifespan)

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
    await session.flush()
    await session.commit()
    return {'message': f'Персонажу присвоен ID {new_character.id}'}


@app.get('/all_characters', tags=['DATABASE'])
async def show_characters(session: SessionDep):
    query = select(CharacterModel).order_by(CharacterModel.id)
    result = await session.execute(query)
    return result.scalars().all()


@app.get('/character_info_by_id', tags=['DATABASE'])
async def get_character(session: SessionDep, character_id: int):
    query = select(CharacterModel).where(CharacterModel.id == character_id)
    result = await session.execute(query)
    return result.scalars().first()

@app.post('/battle', tags=['BATTLE'])
async def battle(session: SessionDep, data: Annotated[Battle, Depends()]):
    result = await do_damage(session, data)
    return result

@app.post('/heal_all', tags=['BATTLE'])
async def heal_all_chars(session: SessionDep):
    await heal_all(session)
    return {'message': 'ALL HEALED'}

# if __name__ == '__main__':
#     uvicorn.run("main:app", reload=True)
