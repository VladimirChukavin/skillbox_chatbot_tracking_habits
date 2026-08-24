"""
Сервис для аутентификации пользователей и управления JWT-токенами.

Содержит функции для проверки учётных данных пользователя и генерации
новой пары access/refresh токенов.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_token, verify_password
from app.models.user_model import User
from app.services.user_services.get_user_by_telegram_id_service import (
    get_user_by_telegram_id,
)
from app.services.user_services.update_refresh_token_service import update_refresh_token


async def authenticate_user(
    session: AsyncSession, telegram_id: int, password: str
) -> User | None:
    """
    Аутентифицировать пользователя по Telegram ID и паролю.

    Ищет пользователя в БД и проверяет соответствие пароля его хешу.

    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :param telegram_id: Telegram ID пользователя
    :type telegram_id: int
    :param password: Пароль в открытом виде
    :type password: str
    :return: Объект пользователя при успешной аутентификации, иначе None
    :rtype: User | None
    """

    user = await get_user_by_telegram_id(session, telegram_id)

    if user is None or not verify_password(password, user.hashed_password):
        return None

    return user


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
