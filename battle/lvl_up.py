from Schemas.CharacterSchema import CharacterModel


async def gain_xp(attacker: CharacterModel, damage_dealt: int, target_killed: bool) -> str:
    log_msg = ""

    # Базовый опыт за урон (10% от урона)
    xp_gained = damage_dealt * 0.1
    attacker.experience += xp_gained
    log_msg += f"Получено {xp_gained} XP за удар. "

    # Бонус за убийство
    if target_killed:
        kill_bonus = 50
        attacker.experience += kill_bonus
        log_msg += f"Бонус за убийство: {kill_bonus} XP. "

    # Проверка Level Up (порог: уровень * 100)
    xp_to_next_level = attacker.level * 100
    if attacker.experience >= xp_to_next_level:
        attacker.level += 1
        attacker.experience -= xp_to_next_level

        # Прирост характеристик
        attacker.damage += 5
        attacker.current_health = 100  # Полное исцеление при повышении уровня

        log_msg += f"** ПОВЫШЕНИЕ УРОВНЯ! Теперь уровень: {attacker.level}. Характеристики улучшены! **"

    return log_msg