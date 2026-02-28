from sqlalchemy import update
from app.schemas.character_schema import CharacterModel, NonPlayableCharacters
from app.battle.battle_logger import BattleLogger


def apply_class_abilities(attacker: CharacterModel, logger: BattleLogger) -> float:
    """Применяет классовые способности атакующего и возвращает итоговый урон."""
    actual_damage = attacker.damage

    if attacker.char_class == 'mage' and attacker.current_mana >= 10:
        actual_damage += 5 * attacker.level
        attacker.current_mana -= 10
        logger.log_ability_use("Маг скастовал заклинание! ")

    elif attacker.char_class == 'rogue' and attacker.current_mana >= 10:
        actual_damage = (attacker.damage + attacker.level) ** 1.2
        attacker.current_mana -= 10
        logger.log_ability_use("Вор наносит коварный удар! ")

    elif attacker.char_class == 'cleric' and attacker.current_mana >= 10:
        heal_amount = 10 * attacker.level
        if attacker.current_health < attacker.max_health:
            attacker.current_health = min(attacker.max_health, attacker.current_health + heal_amount)
            attacker.current_mana -= 10
            logger.log_ability_use(f"Клерик подлечился до {attacker.current_health} ХП перед атакой! ")
            
    return actual_damage

def handle_counter_attack(attacker: CharacterModel, target: CharacterModel | NonPlayableCharacters, logger: BattleLogger):
    """Рассчитывает и применяет урон от контратаки."""
    counter_damage = max(0, target.damage - attacker.armour)
    attacker.current_health -= counter_damage
    logger.log_counter_attack(counter_damage)

async def update_character_stats(session, attacker, target):
    """Обновляет статы персонажей в базе данных."""
    await session.execute(
        update(CharacterModel)
        .where(CharacterModel.id == attacker.id)
        .values(
            current_health=attacker.current_health,
            current_mana=attacker.current_mana,
            experience=attacker.experience,
            level=attacker.level,
            damage=attacker.damage,
            alive=(attacker.current_health > 0)
        )
    )
    if target:
        await session.execute(
            update(CharacterModel)
            .where(CharacterModel.id == target.id)
            .values(current_health=target.current_health, alive=(target.current_health > 0))
        )
    await session.commit()

def are_characters_alive(attacker, target):
    """Проверяет, живы ли персонажи, и возвращает сообщение, если кто-то мертв."""
    if attacker.current_health <= 0:
        return f'Мертвецы не кусаются...'
    if target and target.current_health <= 0:
        return f'Персонаж уже мертв! Оставь вялый труп в покое...'
    return None
