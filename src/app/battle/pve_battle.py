from app.schemas.character_schema import DamageData
from app.battle.battle_logic import create_creep
from app.battle.do_damage import do_damage

async def fight_creep(session, attacker_id: int):
    """
    Координирует бой игрока со случайно созданным крипом.
    Теперь эта функция также отвечает за commit транзакции.
    """
    # 1. Создаем крипа
    creep = await create_creep(session)
    
    # 2. Создаем структуру данных для функции do_damage
    damage_data = DamageData(id_self=attacker_id, id_target=creep.id)
    
    # 3. Проводим бой. do_damage больше не делает commit.
    battle_log = await do_damage(session, damage_data)
    
    # 4. Проверяем состояние крипа. Объект creep все еще в сессии и его состояние актуально.
    if not creep.alive:
        # Помечаем крипа для удаления (это синхронная операция)
        session.delete(creep)
        battle_log += f" Огр повержен и его тело исчезает."
    
    # 5. Завершаем транзакцию (а вот это асинхронная операция)
    await session.commit()
        
    return battle_log
