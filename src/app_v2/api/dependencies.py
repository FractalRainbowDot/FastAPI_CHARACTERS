from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app_v2.core.database import get_player_session, get_npc_session
from app_v2.repositories.character_repository import CharacterRepository
from app_v2.repositories.npc_repository import NpcRepository
from app_v2.services.character_service import CharacterService
from app_v2.services.npc_service import NpcService
from app_v2.services.battle_service import BattleService


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
