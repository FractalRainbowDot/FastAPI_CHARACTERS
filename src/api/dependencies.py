from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_player_session, get_npc_session
from src.repositories.character_repository import CharacterRepository
from src.repositories.npc_repository import NpcRepository
from src.services.character_service import CharacterService
from src.services.npc_service import NpcService
from src.services.battle_service import BattleService
from src.services.database_service import DatabaseService


def get_character_service(session: AsyncSession = Depends(get_player_session)) -> CharacterService:
    return CharacterService(CharacterRepository(session))


def get_npc_service(session: AsyncSession = Depends(get_npc_session)) -> NpcService:
    return NpcService(NpcRepository(session))


def get_battle_service(
        player_session: AsyncSession = Depends(get_player_session),
        npc_session: AsyncSession = Depends(get_npc_session)
) -> BattleService:
    return BattleService(
        CharacterRepository(player_session),
        NpcRepository(npc_session)
    )

def get_database_service() -> DatabaseService:
    return DatabaseService()
