from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.queries import hello_count_players, bye_count_players
from app.routers.router import router_DB, router_battle, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager = asynccontextmanager(get_session)

    print(f'{"Запуск приложения":-^100}')
    async with session_manager() as session:
        count = await hello_count_players(session)
        print(f'В базе {count} игроков')

    yield

    print(f'{"Выключение":-^100}')
    async with session_manager() as session:
        count = await bye_count_players(session)
        print(f'В живых осталось {count} игроков')


app = FastAPI(lifespan=lifespan)
app.include_router(router_DB)
app.include_router(router_battle)
