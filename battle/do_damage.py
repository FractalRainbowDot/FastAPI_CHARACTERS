from fastapi import HTTPException
from sqlalchemy import select, update

from Schemas.CharacterSchema import CharacterModel


async def do_damage(session, data):
    """Тест на дурика"""
    if data.id_self == data.id_target:
        raise HTTPException(status_code=403, detail='Одумайся, роскомнадзорнуться на моем бэке не получится')

    """Получаем статы атакующего (Урон и ХП)"""
    query_attacker = select(CharacterModel.damage, CharacterModel.health).where(CharacterModel.id == data.id_self)
    result_attacker = await session.execute(query_attacker)
    attacker_damage, attacker_health = result_attacker.first()

    """Получаем статы цели (Урон и ХП)"""
    query_target = select(CharacterModel.damage, CharacterModel.health).where(CharacterModel.id == data.id_target)
    result_target = await session.execute(query_target)
    target_damage, target_health = result_target.first()

    """Тест на живучесть до начала боя"""
    if attacker_health <= 0:
        return f'Персонаж {data.id_self} мертв и махать кулаками уже не может...'
    if target_health <= 0:
        return f'Персонаж {data.id_target} уже мертв! Оставь вялый труп в покое...'

    """РАУНД 1: Атакующий бьет цель"""
    target_health -= attacker_damage
    target_is_alive = target_health > 0

    log_message = f'Пользователь {data.id_self} нанес {attacker_damage} урона. '

    """РАУНД 2: Ответный удар (если цель выжила)"""
    attacker_is_alive = True
    if target_is_alive:
        attacker_health -= target_damage
        attacker_is_alive = attacker_health > 0
        log_message += f'Выживший {data.id_target} дал сдачи на {target_damage} урона! '

        if not attacker_is_alive:
            log_message += f'Атакующий {data.id_self} отлетел от ответки...'
    else:
        log_message += f'Цель {data.id_target} пала смертью храбрых и не смогла ответить.'

    """Обновляем состояние цели в БД"""
    query_update_target = (
        update(CharacterModel)
        .where(CharacterModel.id == data.id_target)
        .values(health=target_health, alive=target_is_alive)
    )
    await session.execute(query_update_target)

    """Обновляем состояние атакующего в БД (если ему прилетело)"""
    if target_is_alive:
        query_update_attacker = (
            update(CharacterModel)
            .where(CharacterModel.id == data.id_self)
            .values(health=attacker_health, alive=attacker_is_alive)
        )
        await session.execute(query_update_attacker)

    """Фиксируем изменения"""
    await session.commit()

    return log_message
