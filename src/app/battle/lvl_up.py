from app.schemas.character_schema import CharacterModel, NonPlayableCharacters
from app.battle.battle_logger import BattleLogger

def _calculate_and_apply_xp(attacker: CharacterModel | NonPlayableCharacters,
                            logger: BattleLogger,
                            npc_death_reward: float = 0,
                            damage_dealt: float = 0,
                            ):
    """Рассчитывает и начисляет опыт."""
    xp_gained = damage_dealt // 2 + npc_death_reward
    log_msg = f"Получено {xp_gained} опыта. "
    
    attacker.experience += xp_gained
    logger.log_xp(log_msg)

def _check_and_apply_level_up(attacker: CharacterModel | NonPlayableCharacters, logger: BattleLogger):
    """Проверяет и применяет повышение уровня, если необходимо."""
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

        logger.log_level_up(f"** ПОВЫШЕНИЕ УРОВНЯ! Теперь уровень {attacker.name}: {attacker.level}. Характеристики улучшены! **")

async def gain_xp(
        attacker: CharacterModel | NonPlayableCharacters,
        logger: BattleLogger,
        damage_dealt: float = 0,
        npc_death_reward: float = 0,
):
    _calculate_and_apply_xp(attacker=attacker,
                            damage_dealt=damage_dealt,
                            logger=logger,
                            npc_death_reward=npc_death_reward)
    _check_and_apply_level_up(attacker, logger)
