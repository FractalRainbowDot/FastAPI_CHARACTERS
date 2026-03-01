"""Логика генерации статов NPC"""
from app_v2.repositories.npc_repository import NpcRepository
from app_v2.db_models.npc import NonPlayableCharacters


class NpcService:
    def __init__(self, repo: NpcRepository):
        self.repo = repo

    async def get_or_create_npc(self, level: int) -> NonPlayableCharacters:
        if level < 1:
            raise ValueError('Неправильный ввод уровня')

        npc = await self.repo.get_by_level(level)

        # Если NPC есть, просто воскрешаем его, если он мертв
        if npc:
            if npc.current_health <= 0:
                npc.current_health = npc.max_health
                await self.repo.update(npc)
            return npc

        # Если нет - считаем статы и создаем
        cr_health = 50 * ((1 + 0.1) ** (level - 1))
        cr_dmg = 4 + 1 * (level ** 1.2)
        cr_armour = 2 * (level ** 1.1)
        exp_reward = 10 * (level ** 2)

        new_npc = NonPlayableCharacters(
            level=level,
            max_health=cr_health,
            damage=cr_dmg,
            armour=cr_armour,
            current_health=cr_health,
            exp_reward=exp_reward
        )
        return await self.repo.create(new_npc)
