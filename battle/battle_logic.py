import random
from sqlalchemy import update
from Schemas.CharacterSchema import CharacterModel
from battle.battle_logger import BattleLogger

async def create_creep(session) -> CharacterModel:
    """Создает случайного крипа 'Огр' и сохраняет его в БД."""
    ogre = CharacterModel(
        name="Ogre",
        char_class="monster",
        level=random.randint(1, 3),
        damage=random.randint(8, 15),
        armour=random.randint(2, 8),
        max_health=random.randint(50, 80),
        current_health=1,  # Will be set to max_health below
        max_mana=0,
        current_mana=0,
        experience=0,
        alive=True
    )
    ogre.current_health = ogre.max_health
    
    session.add(ogre)
    await session.flush()
    await session.refresh(ogre)
    return ogre

def apply_class_abilities(attacker: CharacterModel, logger: BattleLogger) -> int:
    """Применяет классовые способности атакующего и возвращает итоговый урон."""
    actual_damage = attacker.damage

    if attacker.char_class == 'mage' and attacker.current_mana >= 10:
        actual_damage += 5
        attacker.current_mana -= 10
        logger.log_ability_use("Маг скастовал заклинание! ")

    elif attacker.char_class == 'rogue' and attacker.current_mana >= 10:
        actual_damage *= 2
        attacker.current_mana -= 10
        logger.log_ability_use("Вор наносит коварный двойной удар! ")

    elif attacker.char_class == 'cleric' and attacker.current_mana >= 10:
        heal_amount = 20
        if attacker.current_health < attacker.max_health:
            attacker.current_health = min(attacker.max_health, attacker.current_health + heal_amount)
            attacker.current_mana -= 10
            logger.log_ability_use(f"Клерик подлечился до {attacker.current_health} ХП перед атакой! ")
            
    return actual_damage

def handle_counter_attack(attacker: CharacterModel, target: CharacterModel, logger: BattleLogger):
    """Рассчитывает и применяет урон от контратаки."""
    counter_damage = max(0, target.damage - attacker.armour)
    attacker.current_health -= counter_damage
    logger.log_counter_attack(counter_damage)

async def update_character_stats(session, attacker, target):
    """Обновляет статы персонажей в базе данных БЕЗ коммита."""
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
    # УБИРАЕМ COMMIT. Он будет вызываться выше по стеку.
    # await session.commit()

def are_characters_alive(attacker, target):
    """Проверяет, живы ли персонажи, и возвращает сообщение, если кто-то мертв."""
    if attacker.current_health <= 0:
        return f'Мертвецы не кусаются...'
    if target and target.current_health <= 0:
        return f'Персонаж уже мертв! Оставь вялый труп в покое...'
    return None
