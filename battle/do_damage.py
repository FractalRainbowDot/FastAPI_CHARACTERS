from fastapi import HTTPException
from sqlalchemy import select, update

from Schemas.CharacterSchema import CharacterModel
from battle.lvl_up import gain_xp


async def do_damage(session, data):
    """Тест на дурика"""
    if data.id_self == data.id_target:
        raise HTTPException(status_code=403, detail='Одумайся, роскомнадзорнуться на моем бэке не получится')

    # Получаем полные объекты атакующего и цели
    attacker = await session.get(CharacterModel, data.id_self)
    target = await session.get(CharacterModel, data.id_target)

    """Тест на живучесть"""
    if attacker.current_health <= 0:
        return f'Мертвецы не кусаются...'
    if target.current_health <= 0:
        return f'Персонаж уже мертв! Оставь вялый труп в покое...'

    # Базовый урон
    actual_damage = attacker.damage
    log_message = ""

    """КЛАССОВЫЕ АБИЛКИ АТАКУЮЩЕГО"""
    if attacker.char_class == 'mage' and attacker.current_mana >= 10:
        actual_damage += 5
        attacker.current_mana -= 10
        log_message += "Маг скастовал заклинание! "

    elif attacker.char_class == 'rogue' and attacker.current_mana >= 10:
        actual_damage *= 2
        attacker.current_mana -= 10
        log_message += "Вор наносит коварный двойной удар! "

    elif attacker.char_class == 'cleric' and attacker.current_mana >= 10:
        if (c_hel := (attacker.current_health + 20)) <= attacker.max_health:
            attacker.current_mana -= 10
            attacker.current_health = c_hel
            log_message += "Клерик подлечился на 20 ХП перед атакой! "

    """БРОНЯ ЦЕЛИ И РАСЧЕТ УРОНА"""
    damage_dealt = max(0, actual_damage - target.armour)
    target.current_health -= damage_dealt

    log_message += f"Пользователь {data.id_self} нанес {damage_dealt} урона пользователю {data.id_target}. "

    """МЕХАНИКА ОПЫТА"""
    is_killed = target.current_health <= 0
    xp_log = await gain_xp(attacker, target, damage_dealt, is_killed)
    log_message += f"Пользователь {data.id_self} нанес {damage_dealt} урона. {xp_log} "

    """МЕХАНИКА КОНТРАТАКИ"""
    if not is_killed:
        counter_damage = max(0, target.damage - attacker.armour)
        attacker.current_health -= counter_damage
        log_message += f"Контратака на {counter_damage} урона! "
    else:
        log_message += f"Пользователь {data.id_target} пал в бою. "

    await session.execute(
        update(CharacterModel)
        .where(CharacterModel.id == attacker.id)
        .values(
            current_health=attacker.current_health,
            current_mana=attacker.current_mana,
            experience=attacker.experience,
            level=attacker.level,
            damage=attacker.damage
        )
    )
    await session.execute(
        update(CharacterModel)
        .where(CharacterModel.id == target.id)
        .values(current_health=target.current_health, alive=(target.current_health > 0))
    )

    await session.commit()
    return log_message