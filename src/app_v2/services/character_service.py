"""Логика создания/удаления персонажей"""
from app_v2.repositories.character_repository import CharacterRepository
from app_v2.db_models.character import CharacterModel
from app_v2.models.character import CharacterAddSchema


class CharacterService:
    def __init__(self, repo: CharacterRepository):
        self.repo = repo

    async def create_character(self, data: CharacterAddSchema) -> CharacterModel:
        base_armour, base_damage = 1, 10

        if data.char_class == 'warrior':
            base_armour += 5
            base_damage -= 3
        elif data.char_class == 'cleric':
            base_damage -= 5

        new_char = CharacterModel(
            name=data.name,
            char_class=data.char_class,
            armour=base_armour,
            damage=base_damage
        )
        return await self.repo.create(new_char)

    async def heal_one(self, character_id: int) -> CharacterModel:
        char = await self.repo.get_by_id(character_id)
        if not char:
            raise ValueError(f"Персонаж с ID {character_id} не найден")

        char.current_health = char.max_health
        char.current_mana = char.max_mana
        char.alive = True
        return await self.repo.update(char)

    async def heal_all(self):
        await self.repo.heal_all()

    async def delete_character(self, character_id: int) -> str:
        success = await self.repo.delete(character_id)
        if not success:
            raise ValueError('Такого персонажа нет')
        return f'Пользователь с ID {character_id} удалён'
