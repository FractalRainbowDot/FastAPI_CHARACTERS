"""Сборка всех роутеров v1"""
from fastapi import APIRouter
from .endpoints import characters, battle, npcs

api_router = APIRouter()

api_router.include_router(characters.router)
api_router.include_router(battle.router)
api_router.include_router(npcs.router)