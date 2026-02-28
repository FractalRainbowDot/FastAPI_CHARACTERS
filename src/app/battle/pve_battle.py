from app.battle.battle_logger import BattleLogger
from app.battle.battle_logic import apply_class_abilities, handle_counter_attack, update_character_stats
from app.database.queries import get_npc_by_lvl, add_creep_to_db, update_npc_stats
from app.schemas.character_schema import CharacterModel
from app.battle.lvl_up import gain_xp


async def fight_creep(session_player, session_npc, attacker: CharacterModel, npc_level):
    
    target_npc = await get_npc_by_lvl(session=session_npc, npc_level=npc_level)
    if not target_npc:
        await add_creep_to_db(npc_level, session_npc)
        target_npc = await get_npc_by_lvl(session=session_npc, npc_level=npc_level)

    if target_npc.current_health <= 0:
        target_npc.current_health = target_npc.max_health
        await update_npc_stats(session_npc, target_npc)

    logger = BattleLogger()
    
    # Атака игрока
    attacker_actual_damage = apply_class_abilities(attacker, logger)
    damage_dealt = max(0, attacker_actual_damage - target_npc.armour)
    target_npc.current_health -= damage_dealt
    logger.log_damage_to_player(attacker.name, target_npc.name, damage_dealt)

    is_killed = target_npc.current_health <= 0
    await gain_xp(attacker=attacker, damage_dealt=damage_dealt, logger=logger)

    # Атака NPC
    if not is_killed:
        handle_counter_attack(attacker, target_npc, logger)
    else:
        logger.log_npc_death(target_npc.name)
        await gain_xp(attacker=attacker, npc_death_reward=target_npc.exp_reward, logger=logger)


    # Сохранение результатов
    await update_character_stats(session_player, attacker, None)
    await update_npc_stats(session_npc, target_npc)
    
    logger.log_final_health(attacker, target_npc)
    
    return logger.get_full_log()
