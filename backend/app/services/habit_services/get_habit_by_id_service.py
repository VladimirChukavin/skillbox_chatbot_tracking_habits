"""
Сервис для получения привычки по идентификатору.

Содержит функцию для поиска конкретной привычки пользователя в базе данных.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_model import Habit


async def get_habit_by_id(
    session: AsyncSession, habit_id: int, user_id: int
) -> Habit | None:
    """
    Получить привычку по её ID с проверкой принадлежности пользователю.

    Выполняет запрос к БД, фильтруя записи одновременно по ID привычки
    и ID пользователя, что исключает возможность получить чужую привычку.

    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :param habit_id: Идентификатор искомой привычки
    :type habit_id: int
    :param user_id: Идентификатор пользователя-владельца
    :type user_id: int
    :return: Объект привычки или None, если привычка не найдена
    :rtype: Habit | None
    """

    result = await session.execute(
        select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    )

    return result.scalar_one_or_none()
