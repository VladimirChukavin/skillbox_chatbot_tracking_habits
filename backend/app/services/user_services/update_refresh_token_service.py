"""
Сервис для обновления refresh-токена пользователя.

Содержит функцию для сохранения нового refresh-токена в базе данных
при успешной аутентификации или обновлении access-токена.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User


async def update_refresh_token(
    session: AsyncSession, user_id: int, refresh_token: str
) -> None:
    """
    Обновить refresh-токен для указанного пользователя.

    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :param user_id: Идентификатор пользователя
    :type user_id: int
    :param refresh_token: Новый refresh-токен для сохранения
    :type refresh_token: str
    :return: Ничего не возвращает
    :rtype: None
    """

    user = await session.get(User, user_id)

    if user is not None:
        user.refresh_token = refresh_token
