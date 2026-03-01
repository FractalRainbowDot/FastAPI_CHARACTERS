from contextlib import asynccontextmanager
from fastapi import FastAPI

from app_v2.api.v1.router import api_router
from app_v2.core.database import player_session_maker
from app_v2.repositories.character_repository import CharacterRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f'{"Запуск приложения":-^100}')

    # Запрашиваем количество игроков при старте через репозиторий
    async with player_session_maker() as session:
        repo = CharacterRepository(session)
        count = await repo.count_all()
        print(f'В базе {count} игроков')

    yield

    print(f'{"Выключение":-^100}')

    # Запрашиваем количество живых при выключении
    async with player_session_maker() as session:
        repo = CharacterRepository(session)
        count = await repo.count_alive()
        print(f'В живых осталось {count} игроков')


app = FastAPI(
    title="RPG Battle API (Clean Architecture)",
    description="Обновленная версия API с разделением на слои",
    version="2.0.0",
    lifespan=lifespan
)

# Подключаем всю маршрутизацию одним вызовом
app.include_router(api_router, prefix="/api/v1")
