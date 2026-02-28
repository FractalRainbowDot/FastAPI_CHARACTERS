from Schemas.CharacterSchema import CharacterModel
from battle.battle_logger import BattleLogger

def _calculate_and_apply_xp(attacker: CharacterModel, target: CharacterModel, damage_dealt: int, target_killed: bool, logger: BattleLogger):
    """Рассчитывает и начисляет опыт."""
    xp_gained = damage_dealt // 10
    log_msg = f"Получено {xp_gained} XP за удар. "

    if target_killed:
        kill_bonus = 10 * target.level
        xp_gained += kill_bonus
        log_msg += f"Бонус за убийство: {kill_bonus} XP. "
    
    attacker.experience += xp_gained
    logger.log_xp(log_msg)

def _check_and_apply_level_up(attacker: CharacterModel, logger: BattleLogger):
    """Проверяет и применяет повышение уровня, если необходимо."""
    xp_to_next_level = attacker.level * 100
    if attacker.experience >= xp_to_next_level:
        attacker.level += 1
        attacker.experience -= xp_to_next_level

        # Прирост характеристик
        attacker.damage += 5
        attacker.max_health += 15
        attacker.max_mana += 10
        attacker.current_health = attacker.max_health
        attacker.current_mana = attacker.max_mana

        logger.log_level_up(f"** ПОВЫШЕНИЕ УРОВНЯ! Теперь уровень: {attacker.level}. Характеристики улучшены! **")

async def gain_xp(
        attacker: CharacterModel,
        target: CharacterModel,
        damage_dealt: int,
        target_killed: bool,
        logger: BattleLogger
):
    """Координирует получение опыта и повышение уровня."""
    _calculate_and_apply_xp(attacker, target, damage_dealt, target_killed, logger)
    _check_and_apply_level_up(attacker, logger)
