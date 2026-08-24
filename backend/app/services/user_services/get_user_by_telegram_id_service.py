"""
Сервис для поиска пользователя по Telegram ID.

Содержит функцию для получения объекта пользователя из базы данных
на основе его уникального идентификатора в Telegram.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User


async def get_user_by_telegram_id(
    session: AsyncSession, telegram_id: int
) -> User | None:
    """
    Получить пользователя по его Telegram ID.

    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :param telegram_id: Уникальный Telegram ID пользователя
    :type telegram_id: int
    :return: Объект пользователя или None, если пользователь не найден
    :rtype: User | None
    """

    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()
