from sqlalchemy import select, update

from Shemas.CharacterShema import CharacterModel


async def do_damage(session, data):
    query_damage = select(CharacterModel.damage).where(CharacterModel.id == data.id_self)
    result_damage = await session.execute(query_damage)
    damage_value = result_damage.scalar()
    query_target_health = (
        select(CharacterModel.health).
        where(CharacterModel.id == data.id_target))
    result_target_health = await session.execute(query_target_health)
    target_health = result_target_health.scalar()
    if target_health <= 0:
        return f'Персонаж уже мертв! Оставь вялый труп в покое...'
    target_health -= damage_value
    if target_health <= 0:
        query = (update(CharacterModel)
                 .where(CharacterModel.id == data.id_target)
                 .values(alive=False))
        await session.execute(query)
    query_update = (
        update(CharacterModel)
        .where(CharacterModel.id == data.id_target)
        .values(health=target_health))
    await session.execute(query_update)
    await session.commit()
    return f'пользователь {data.id_self} нанес {damage_value} урона пользователю {data.id_target}'
