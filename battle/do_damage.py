from fastapi import HTTPException
from sqlalchemy import select, update

from Schemas.CharacterSchema import CharacterModel


async def do_damage(session, data):
    """Тест на дурика"""
    if data.id_self == data.id_target:
        raise HTTPException(status_code=403, detail='Одумайся, роскомнадзорнуться на моем бэке не получится')

    # Получаем полные объекты атакующего и цели
    attacker = await session.get(CharacterModel, data.id_self)
    target = await session.get(CharacterModel, data.id_target)

    """Тест на живучесть"""
    if attacker.health <= 0:
        return f'Мертвецы не кусаются...'
    if target.health <= 0:
        return f'Персонаж уже мертв! Оставь вялый труп в покое...'

    # Базовый урон
    actual_damage = attacker.damage
    log_message = ""

    """КЛАССОВЫЕ АБИЛКИ АТАКУЮЩЕГО"""
    if attacker.char_class == 'mage' and attacker.mana >= 10:
        actual_damage += 5
        attacker.mana -= 10
        log_message += "Маг скастовал заклинание! "

    elif attacker.char_class == 'rogue' and attacker.mana >= 10:
        actual_damage *= 2
        attacker.mana -= 10
        log_message += "Вор наносит коварный двойной удар! "

    elif attacker.char_class == 'cleric' and attacker.mana >= 10:
        attacker.health += 20
        attacker.mana -= 10
        log_message += "Клерик подлечился на 20 ХП перед атакой! "

    """БРОНЯ ЦЕЛИ И РАСЧЕТ УРОНА"""
    # Урон режется об показатель брони (но не может быть меньше 0)
    damage_dealt = max(0, actual_damage - target.armour)
    target.health -= damage_dealt

    log_message += f"Пользователь {data.id_self} нанес {damage_dealt} урона пользователю {data.id_target}. "

    """МЕХАНИКА КОНТРАТАКИ"""
    if target.health > 0:
        # Если цель выжила, она бьет в ответ
        # Урон цели режется об броню изначального атакующего
        counter_damage_dealt = max(0, target.damage - attacker.armour)
        attacker.health -= counter_damage_dealt
        log_message += f"Пользователь {data.id_target} выжил и провел контратаку, нанеся {counter_damage_dealt} урона! "
    else:
        log_message += f"Пользователь {data.id_target} был убит этим ударом. "

    """Обновление состояния атакующего (ведь он мог потратить ману или отхилиться)"""
    query_update_attacker = (
        update(CharacterModel)
        .where(CharacterModel.id == data.id_self)
        .values(health=attacker.health, mana=attacker.mana)
    )
    await session.execute(query_update_attacker)

    """Обновление состояния цели"""
    is_alive = target.health > 0
    query_update_target = (
        update(CharacterModel)
        .where(CharacterModel.id == data.id_target)
        .values(health=target.health, alive=is_alive)
    )
    await session.execute(query_update_target)

    await session.commit()
    return log_message