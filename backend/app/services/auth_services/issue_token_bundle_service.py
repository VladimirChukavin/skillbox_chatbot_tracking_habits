"""
Сервис для управления JWT-токенами.

Содержит функции для генерации новой пары access/refresh токенов.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_token
from app.models.user_model import User
from app.services.user_services.update_refresh_token_service import (
    update_refresh_token,
)


async def issue_token_bundle(session: AsyncSession, user: User) -> dict[str, str]:
    """
    Сгенерировать и сохранить пару access/refresh токенов для пользователя.

    Создаёт новые JWT-токены и сохраняет refresh-токен в БД для возможности
    его дальнейшего обновления и отзыва.

    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :param user: Объект пользователя для генерации токенов
    :type user: User
    :return: Словарь с access_token, refresh_token и token_type
    :rtype: dict[str, str]
    """

    access_token = create_token(user.telegram_id, user.id, token_type="access")
    refresh_token = create_token(user.telegram_id, user.id, token_type="refresh")

    await update_refresh_token(session, user.id, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
