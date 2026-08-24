"""
Сервис для создания новой привычки.

Содержит функцию для добавления привычки в базу данных с учётом
часового пояса пользователя при установке времени напоминания.
"""

import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_model import Habit
from app.models import User
from app.schemas.habit_schema import HabitCreate


async def create_habit(
    session: AsyncSession, user_id: int, payload: HabitCreate, user: User
) -> Habit:
    """
    Создать новую привычку для пользователя.

    Если в данных передано время напоминания reminder_time, оно
    конвертируется из локального часового пояса пользователя в UTC
    перед сохранением в базу данных.

    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :param user_id: Идентификатор пользователя
    :type user_id: int
    :param payload: Данные для создания привычки
    :type payload: HabitCreate
    :param user: Объект пользователя (для получения часового пояса)
    :type user: User
    :return: Созданный объект привычки
    :rtype: Habit
    """

    reminder_time = payload.reminder_time

    if reminder_time is not None:
        tz = ZoneInfo(user.timezone)
        naive = datetime.datetime.combine(datetime.date.today(), reminder_time)
        aware = naive.replace(tzinfo=tz)
        reminder_time = aware.astimezone(datetime.timezone.utc).time().replace(second=0)

    habit = Habit(
        user_id=user_id,
        title=payload.title,
        description=payload.description,
        target_description=payload.target_description,
        target_days=payload.target_days,
        reminder_time=reminder_time,
    )

    session.add(habit)
    await session.flush()

    return habit
