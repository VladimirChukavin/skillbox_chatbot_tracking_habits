"""
Сервис для получения списка привычек пользователя.

Содержит функцию для выборки всех или только активных привычек
конкретного пользователя из базы данных.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_model import Habit


async def get_habits_by_user(
    session: AsyncSession, user_id: int, active_only: bool = True
) -> list[Habit]:
    """
    Получить список привычек пользователя, отсортированных по дате создания.

    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :param user_id: Идентификатор пользователя
    :type user_id: int
    :param active_only: Флаг фильтрации только активных привычек (по умолчанию True)
    :type active_only: bool
    :return: Список объектов привычек, отсортированных по возрастанию даты создания
    :rtype: list[Habit]
    """

    statement = select(Habit).where(Habit.user_id == user_id)

    if active_only:
        statement = statement.where(Habit.is_active.is_(True))

    statement = statement.order_by(Habit.created_at.asc())
    result = await session.execute(statement)

    return list(result.scalars().all())
