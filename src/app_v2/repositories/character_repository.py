"""Запросы к таблице characters"""
from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app_v2.db_models.character import CharacterModel


class CharacterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def count_all(self) -> int:
        query = func.count(CharacterModel.id)
        result = await self.session.execute(query)
        return result.scalar()

    async def count_alive(self) -> int:
        query = select(func.count(CharacterModel.id)).where(CharacterModel.alive == True)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_by_id(self, character_id: int) -> CharacterModel | None:
        query = select(CharacterModel).where(CharacterModel.id == character_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_for_update(self, character_id: int) -> CharacterModel | None:
        # Специальный метод с блокировкой строки для боев (заменяет with_for_update из do_damage)
        query = select(CharacterModel).where(CharacterModel.id == character_id).with_for_update()
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_all(self) -> list[CharacterModel]:
        query = select(CharacterModel).order_by(CharacterModel.id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, character: CharacterModel) -> CharacterModel:
        # Репозиторий получает УЖЕ готовый объект с рассчитанными статами и просто сохраняет его
        self.session.add(character)
        await self.session.commit()
        await self.session.refresh(character)
        return character

    async def update(self, character: CharacterModel) -> CharacterModel:
        self.session.add(character)
        await self.session.commit()
        await self.session.refresh(character)
        return character

    async def delete(self, character_id: int) -> bool:
        query = delete(CharacterModel).where(CharacterModel.id == character_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0

    async def heal_all(self) -> None:
        # Прямой UPDATE переехал сюда из heal.py
        query = update(CharacterModel).values(
            current_health=CharacterModel.max_health,
            current_mana=CharacterModel.max_mana,
            alive=True
        )
        await self.session.execute(query)
        await self.session.commit()
