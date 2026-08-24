"""
Сервис для обновления данных привычки.

Содержит функцию для частичного обновления полей привычки с учётом
часового пояса пользователя при изменении времени напоминания.
"""

import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_model import Habit
from app.models import User
from app.schemas.habit_schema import HabitUpdate


async def update_habit(
    session: AsyncSession, habit: Habit, payload: HabitUpdate, user: User
) -> Habit:
    """
    Частично обновить данные привычки.

    Принимает только те поля, которые были переданы в запросе (exclude_unset).
    Если обновляется время напоминания reminder_time, оно конвертируется
    из локального часового пояса пользователя в UTC перед сохранением.

    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :param habit: Объект обновляемой привычки
    :type habit: Habit
    :param payload: Данные для обновления
    :type payload: HabitUpdate
    :param user: Объект пользователя (для получения часового пояса)
    :type user: User
    :return: Обновлённый объект привычки
    :rtype: Habit
    """

    update_data = payload.model_dump(exclude_unset=True)

    if "reminder_time" in update_data and update_data["reminder_time"] is not None:
        local_time = update_data["reminder_time"]
        tz = ZoneInfo(user.timezone)
        naive = datetime.datetime.combine(datetime.date.today(), local_time)
        aware = naive.replace(tzinfo=tz)
        utc_time = aware.astimezone(datetime.timezone.utc).time().replace(second=0)
        update_data["reminder_time"] = utc_time

    for field, value in update_data.items():
        setattr(habit, field, value)

    await session.flush()

    return habit
