"""Координация ударов, расчет урона"""
from src.repositories.character_repository import CharacterRepository
from src.repositories.npc_repository import NpcRepository
from src.services.npc_service import NpcService
from src.services.battle_logger import BattleLogger
from src.services.experience_service import ExperienceService


class BattleService:
    def __init__(self, char_repo: CharacterRepository, npc_repo: NpcRepository):
        self.char_repo = char_repo
        self.npc_repo = npc_repo
        self.npc_service = NpcService(npc_repo)

    def _apply_class_abilities(self, attacker, logger: BattleLogger) -> float:
        actual_damage = attacker.damage
        if attacker.char_class == 'mage' and attacker.current_mana >= 10:
            actual_damage += 5 * attacker.level
            attacker.current_mana -= 10
            logger.log_ability_use("Маг скастовал заклинание! ")
        elif attacker.char_class == 'rogue' and attacker.current_mana >= 10:
            actual_damage = (attacker.damage + attacker.level) ** 1.2
            attacker.current_mana -= 10
            logger.log_ability_use("Вор наносит коварный удар! ")
        elif attacker.char_class == 'cleric' and attacker.current_mana >= 10:
            heal_amount = 10 * attacker.level
            if attacker.current_health < attacker.max_health:
                attacker.current_health = min(attacker.max_health, attacker.current_health + heal_amount)
                attacker.current_mana -= 10
                logger.log_ability_use(f"Клерик подлечился до {attacker.current_health} ХП перед атакой! ")
        return actual_damage

    def _handle_counter_attack(self, attacker, target, logger: BattleLogger):
        counter_damage = max(0, target.damage - attacker.armour)
        attacker.current_health -= counter_damage
        logger.log_counter_attack(counter_damage)

    def _are_characters_alive(self, attacker, target) -> str | None:
        if attacker.current_health <= 0:
            return 'Мертвецы не кусаются...'
        if target and target.current_health <= 0:
            return 'Персонаж уже мертв! Оставь вялый труп в покое...'
        return None

    async def pvp_battle(self, attacker_id: int, target_id: int) -> str:
        if attacker_id == target_id:
            raise ValueError('Себя не трогай на публике')

        # Запрашиваем с блокировкой строк (with_for_update)
        attacker = await self.char_repo.get_for_update(attacker_id)
        target = await self.char_repo.get_for_update(target_id)

        if not attacker or not target:
            raise ValueError("Один из персонажей не найден")

        if message := self._are_characters_alive(attacker, target):
            return message

        logger = BattleLogger()
        actual_damage = self._apply_class_abilities(attacker, logger)
        damage_dealt = max(0, actual_damage - target.armour)
        target.current_health -= damage_dealt
        logger.log_damage_to_player(attacker.name, target.name, damage_dealt)

        is_killed = target.current_health <= 0
        ExperienceService.gain_xp(attacker, logger, damage_dealt=damage_dealt)

        if not is_killed:
            self._handle_counter_attack(attacker, target, logger)
        else:
            logger.log_death(target.name)
            target.alive = False

        if attacker.current_health <= 0:
            attacker.alive = False

        await self.char_repo.update(attacker)
        await self.char_repo.update(target)
        logger.log_final_health(attacker, target)
        return logger.get_full_log()

    async def pve_battle(self, attacker_id: int, npc_level: int) -> str:
        attacker = await self.char_repo.get_by_id(attacker_id)
        if not attacker:
            raise ValueError(f"Игрок с ID {attacker_id} не найден")

        target_npc = await self.npc_service.get_or_create_npc(npc_level)

        if message := self._are_characters_alive(attacker, target_npc):
            return message

        logger = BattleLogger()
        actual_damage = self._apply_class_abilities(attacker, logger)
        damage_dealt = max(0, actual_damage - target_npc.armour)
        target_npc.current_health -= damage_dealt
        logger.log_damage_to_player(attacker.name, target_npc.name, damage_dealt)

        is_killed = target_npc.current_health <= 0
        ExperienceService.gain_xp(attacker, logger, damage_dealt=damage_dealt)

        if not is_killed:
            self._handle_counter_attack(attacker, target_npc, logger)
        else:
            logger.log_npc_death(target_npc.name)
            ExperienceService.gain_xp(attacker, logger, npc_death_reward=target_npc.exp_reward)

        if attacker.current_health <= 0:
            attacker.alive = False

        await self.char_repo.update(attacker)
        await self.npc_repo.update(target_npc)
        logger.log_final_health(attacker, target_npc)
        return logger.get_full_log()
