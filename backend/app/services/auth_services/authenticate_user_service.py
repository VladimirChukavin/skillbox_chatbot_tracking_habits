"""
Сервис для аутентификации пользователей.

Содержит функции для проверки учётных данных пользователя.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.models.user_model import User
from app.services.user_services.get_user_by_telegram_id_service import (
    get_user_by_telegram_id,
)


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
