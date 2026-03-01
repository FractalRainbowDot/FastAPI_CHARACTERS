# src/services/database_service.py
from sqlalchemy.ext.asyncio import AsyncEngine

from src.core.database import player_engine, npc_engine
from src.db_models.character import CharacterModel
from src.db_models.npc import NonPlayableCharacters


class DatabaseService:
    def __init__(
        self,
        p_engine: AsyncEngine = player_engine,
        n_engine: AsyncEngine = npc_engine,
    ):
        self.player_engine = p_engine
        self.npc_engine = n_engine

    async def recreate_databases(self) -> None:
        """
        Удаляет и создает заново таблицы для всех баз данных.
        """
        # Работаем с БД игроков
        async with self.player_engine.begin() as conn:
            await conn.run_sync(CharacterModel.metadata.drop_all)
            await conn.run_sync(CharacterModel.metadata.create_all)

        # Работаем с БД NPC
        async with self.npc_engine.begin() as conn:
            await conn.run_sync(NonPlayableCharacters.metadata.drop_all)
            await conn.run_sync(NonPlayableCharacters.metadata.create_all)
