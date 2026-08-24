"""
Главный агрегирующий роутер приложения.

Объединяет все доменные роутеры (аутентификации, привычек и пользователя)
в единую точку входа для последующего подключения к экземпляру FastAPI.
"""

from fastapi import APIRouter

from app.api.auth_routers import auth_router
from app.api.habits_routers import habits_router
from app.api.user_routers import user_router

main_router = APIRouter()

main_router.include_router(auth_router.main_auth_router)
main_router.include_router(habits_router.main_habits_router)
main_router.include_router(user_router.router)
