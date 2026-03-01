"""Запросы к таблице NonPlayableCharacters"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db_models.npc import NonPlayableCharacters


class NpcRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_level(self, level: int) -> NonPlayableCharacters | None:
        query = select(NonPlayableCharacters).where(NonPlayableCharacters.level == level)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create(self, npc: NonPlayableCharacters) -> NonPlayableCharacters:
        self.session.add(npc)
        await self.session.commit()
        await self.session.refresh(npc)
        return npc

    async def update(self, npc: NonPlayableCharacters) -> NonPlayableCharacters:
        self.session.add(npc)
        await self.session.commit()
        await self.session.refresh(npc)
        return npc
