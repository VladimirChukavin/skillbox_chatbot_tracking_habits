"""
Роутер для аутентификации пользователя по Telegram ID и паролю.

Обеспечивает endpoint для входа в систему через JSON-тело запроса.
Используется Telegram-ботом для получения JWT-токенов.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.token_schema import TokenBundle
from app.schemas.user_schema import UserLogin
from app.database import get_db_session
from app.services.auth_services.authenticate_user_service import authenticate_user
from app.services.auth_services.issue_token_bundle_service import issue_token_bundle

router = APIRouter()


@router.post("/login", response_model=TokenBundle)
async def login_user(
    payload: UserLogin, session: AsyncSession = Depends(get_db_session)
) -> dict:
    """
    Аутентифицировать пользователя по Telegram ID и паролю.

    Принимает данные в формате JSON (telegram_id и password),
    проверяет учётные данные и возвращает пару access/refresh токенов.

    :param payload: Данные для входа (telegram_id, password)
    :type payload: UserLogin
    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :raises HTTPException: 401 — если неверный Telegram ID или пароль
    :return: Словарь с access и refresh токенами
    :rtype: dict
    """

    user = await authenticate_user(session, payload.telegram_id, payload.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный Telegram ID или пароль",
        )

    return await issue_token_bundle(session, user)
