from typing import Annotated

from fastapi import APIRouter, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from Shemas.CharacterShema import Base, CharacterAddShema, CharacterModel, Battle
from battle.do_damage import do_damage
from battle.heal_all import heal_all

router_battle = APIRouter(
    prefix='/battle',
    tags=['BATTLE'],
)

router_DB = APIRouter(
    prefix='/battle',
    tags=['DATABASE'],
)

engine = create_async_engine('sqlite+aiosqlite:///database/characters.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router_DB.post('/create_DB')
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'message': 'ZAEBIS'}


@router_DB.post('/add_character_to_DB')
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


@router_DB.get('/all_characters')
async def show_characters(session: SessionDep):
    query = select(CharacterModel).order_by(CharacterModel.id)
    result = await session.execute(query)
    return result.scalars().all()


@router_DB.get('/character_info_by_id')
async def get_character(session: SessionDep, character_id: int):
    query = select(CharacterModel).where(CharacterModel.id == character_id)
    result = await session.execute(query)
    return result.scalars().first()


@router_battle.post('/do_hit')
async def battle(
        session: SessionDep,
        data: Annotated[Battle, Depends()]
):
    result = await do_damage(session, data)
    return result


@router_battle.post('/heal_all')
async def heal_all_chars(
        session: SessionDep
):
    await heal_all(session)
    return {'message': 'ALL HEALED'}
