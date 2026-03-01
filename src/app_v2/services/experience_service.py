"""Логика начисления опыта и Level Up"""
from app_v2.services.battle_logger import BattleLogger


class ExperienceService:
    @staticmethod
    def gain_xp(attacker, logger: BattleLogger, damage_dealt: float = 0, npc_death_reward: float = 0):
        # Начисляем опыт
        xp_gained = damage_dealt // 2 + npc_death_reward
        attacker.experience += xp_gained
        logger.log_xp(f"Получено {xp_gained} опыта. ")

        # Проверяем Level Up
        xp_to_next_level = attacker.level ** 2.2 * 100
        if attacker.experience >= xp_to_next_level:
            attacker.level += 1
            attacker.experience -= xp_to_next_level

            # Прирост характеристик
            attacker.damage = 5 + (2.5 * (attacker.level ** 1.1))
            attacker.max_health = 100 * (1.12 ** (attacker.level - 1))
            attacker.max_mana += 10
            attacker.armour = 2 * (attacker.level ** 1.1)
            attacker.current_health = attacker.max_health
            attacker.current_mana = attacker.max_mana

            logger.log_level_up(
                f"** ПОВЫШЕНИЕ УРОВНЯ! Теперь уровень {attacker.name}: {attacker.level}. Характеристики улучшены! **")
