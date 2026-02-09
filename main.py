from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.queries import hello_count_players, bye_count_players
from routers.router import router_DB, router_battle, new_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f'{'Запуск приложения':-^100}')
    async with new_session() as session:
        count_players = await hello_count_players(session)
        print(f'К бою готовы {count_players} игроков')
    yield
    print(f'{'Выключение':-^100}')
    async with new_session() as session:
        count_players = await bye_count_players(session)
        print(f'В живых осталось {count_players} игроков')


app = FastAPI(lifespan=lifespan)
app.include_router(router_DB)
app.include_router(router_battle)
