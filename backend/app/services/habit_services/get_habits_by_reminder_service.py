"""
Сервис для получения привычек по времени напоминания.

Содержит функцию для поиска активных привычек, требующих отправки
уведомления в указанное время.
"""

import datetime

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_model import Habit
from app.models import User


async def get_habits_by_reminder(
    session: AsyncSession, reminder_time: datetime.time
) -> list[dict]:
    """
    Получить активные привычки для напоминания на указанное время.

    Выполняет поиск привычек, у которых часы и минуты времени напоминания
    совпадают с переданным значением. Использует соединение с таблицей
    пользователей для получения telegram_id, необходимого боту
    для отправки уведомления.

    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :param reminder_time: Время напоминания (часы и минуты) в UTC
    :type reminder_time: datetime.time
    :return: Список словарей с ключами telegram_id, habit_id и title
    :rtype: list[dict]
    """

    statement = (
        select(Habit, User.telegram_id)
        .join(User, Habit.user_id == User.id)
        .where(Habit.is_active.is_(True))
        .where(Habit.reminder_time.isnot(None))
        .where(sqlalchemy.extract("hour", Habit.reminder_time) == reminder_time.hour)
        .where(
            sqlalchemy.extract("minute", Habit.reminder_time) == reminder_time.minute
        )
    )
    result = await session.execute(statement)

    return [
        {
            "telegram_id": row.telegram_id,
            "habit_id": row.Habit.id,
            "title": row.Habit.title,
        }
        for row in result
    ]
