from fastapi import HTTPException
from app.schemas.character_schema import CharacterModel, DamageData
from app.battle.lvl_up import gain_xp
from app.battle.battle_logic import apply_class_abilities, handle_counter_attack, update_character_stats, are_characters_alive
from app.battle.battle_logger import BattleLogger

async def do_damage(session, data: DamageData):
    """Координирует бой между двумя персонажами с блокировкой строк для избежания race condition."""
    if data.id_self == data.id_target:
        raise HTTPException(status_code=403, detail='Одумайся, роскомнадзорнуться на моем бэке не получится')

    # БЛОКИРУЕМ строки атакующего и цели для эксклюзивного доступа
    attacker = await session.get(CharacterModel, data.id_self, with_for_update=True)
    target = await session.get(CharacterModel, data.id_target, with_for_update=True)

    if not attacker:
        raise HTTPException(status_code=404, detail=f"Атакующий с ID {data.id_self} не найден")
    if not target:
        raise HTTPException(status_code=404, detail=f"Цель с ID {data.id_target} не найдена")

    if message := are_characters_alive(attacker, target):
        return message

    logger = BattleLogger()

    actual_damage = apply_class_abilities(attacker, logger)

    damage_dealt = max(0, actual_damage - target.armour)
    target.current_health -= damage_dealt
    logger.log_damage(attacker.id, target.id, damage_dealt)

    is_killed = target.current_health <= 0
    await gain_xp(attacker, target, damage_dealt, is_killed, logger)

    if not is_killed:
        handle_counter_attack(attacker, target, logger)
    else:
        logger.log_death(target.id)

    # Функция update_character_stats уже делает commit, который снимает блокировку
    await update_character_stats(session, attacker, target)
    
    logger.log_final_health(attacker, target)
    
    return logger.get_full_log()
