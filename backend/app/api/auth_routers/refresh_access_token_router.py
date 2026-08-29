"""
Роутер для обновления access-токена с помощью refresh-токена.

Обеспечивает endpoint для получения новой пары токенов, когда срок
действия access-токена истёк.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.core.security import decode_token
from app.database import get_db_session
from app.schemas.token_schema import TokenBundle
from app.services.auth_services.issue_token_bundle_service import issue_token_bundle
from app.services.user_services.get_user_by_telegram_id_service import (
    get_user_by_telegram_id,
)

router = APIRouter()


@router.post("/refresh", response_model=TokenBundle)
async def refresh_access_token(
    refresh_token: str, session: AsyncSession = Depends(get_db_session)
) -> dict:
    """
    Обновить access-токен, используя refresh-токен.

    Принимает refresh-токен, проверяет его валидность, тип и совпадение
    с токеном, сохранённым в БД. При успехе генерирует и возвращает новую
    пару access/refresh токенов.

    :param refresh_token: Refresh-токен для обновления
    :type refresh_token: str
    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :raises HTTPException: 401 — если токен недействителен, неверного типа
        или отозван (не совпадает с сохранённым в БД)
    :return: Словарь с новыми access и refresh токенами
    :rtype: dict
    """

    try:
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный тип токена",
            )

        telegram_id = int(payload.get("telegram_id"))
    except (JWTError, ValueError, KeyError, TypeError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный refresh-token",
        ) from error

    user = await get_user_by_telegram_id(session, telegram_id)

    if user is None or user.refresh_token != refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh-токен не найден или отозван",
        )

    return await issue_token_bundle(session, user)
