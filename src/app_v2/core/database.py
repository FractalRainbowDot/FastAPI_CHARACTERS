"""Настройка engine и sessionmaker"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# --- База данных для Игроков ---
player_engine = create_async_engine('sqlite+aiosqlite:///src/app_v2/core/data/characters.db')
player_session_maker = async_sessionmaker(player_engine, expire_on_commit=False)

async def get_player_session():
    async with player_session_maker() as session:
        yield session

# --- База данных для NPC ---
npc_engine = create_async_engine('sqlite+aiosqlite:///src/app_v2/core/data/NonPlayableCharacters.db')
npc_session_maker = async_sessionmaker(npc_engine, expire_on_commit=False)

async def get_npc_session():
    async with npc_session_maker() as session:
        yield session