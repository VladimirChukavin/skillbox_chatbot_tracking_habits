"""
Агрегирующий роутер для аутентификации и авторизации.

Объединяет все эндпоинты, связанные с управлением учётными данными
и выдачей JWT-токенов, под общим префиксом /auth.
"""

from fastapi import APIRouter

from app.api.auth_routers import (
    user_register_router,
    login_user_router,
    login_oauth_form_router,
    refresh_access_token_router,
)

main_auth_router = APIRouter(prefix="/auth", tags=["auth"])

main_auth_router.include_router(user_register_router.router)
main_auth_router.include_router(login_user_router.router)
main_auth_router.include_router(login_oauth_form_router.router)
main_auth_router.include_router(refresh_access_token_router.router)
