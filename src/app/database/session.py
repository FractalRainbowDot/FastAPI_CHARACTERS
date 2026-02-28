from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# --- База данных для Игроков ---
player_engine = create_async_engine('sqlite+aiosqlite:///src/app/database/characters.db')
player_session_maker = async_sessionmaker(player_engine, expire_on_commit=False)


async def get_player_session():
    async with player_session_maker() as session:
        yield session

PlayerSessionDep = Annotated[AsyncSession, Depends(get_player_session)]


# --- База данных для NPC ---
npc_engine = create_async_engine('sqlite+aiosqlite:///src/app/database/NonPlayableCharacters.db')
npc_session_maker = async_sessionmaker(npc_engine, expire_on_commit=False)

async def get_npc_session():
    async with npc_session_maker() as session:
        yield session

NpcSessionDep = Annotated[AsyncSession, Depends(get_npc_session)]
