"""
Сервис для отметки выполнения привычки.

Содержит функцию для создания или обновления лога выполнения привычки
за определённый день с автоматической корректировкой счётчика выполнений.
"""

import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_model import Habit
from app.models.habit_log_model import HabitLog


async def track_habit(
    session: AsyncSession,
    habit: Habit,
    is_completed: bool,
    log_date: datetime.date | None = None,
) -> HabitLog:
    """
    Отметить выполнение привычки за указанный день.

    Если запись за этот день уже существует, обновляет её статус.
    При изменении статуса корректирует счётчик выполненных дней completed_count
    у привычки: увеличивает при отметке выполнения или уменьшает при отмене.

    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :param habit: Объект привычки для отметки
    :type habit: Habit
    :param is_completed: Статус выполнения (True — выполнено, False — нет)
    :type is_completed: bool
    :param log_date: Дата отметки (по умолчанию текущий день)
    :type log_date: datetime.date | None
    :return: Объект записи лога выполнения
    :rtype: HabitLog
    """

    target_date = log_date or datetime.date.today()
    result = await session.execute(
        select(HabitLog).where(
            HabitLog.habit_id == habit.id, HabitLog.log_date == target_date
        )
    )
    log_entry = result.scalar_one_or_none()

    if log_entry is None:
        log_entry = HabitLog(
            habit_id=habit.id, log_date=target_date, is_completed=is_completed
        )
        session.add(log_entry)

        if is_completed:
            habit.completed_count += 1
    else:
        if not log_entry.is_completed and is_completed:
            habit.completed_count += 1
        elif log_entry.is_completed and not is_completed:
            habit.completed_count = max(0, habit.completed_count - 1)

        log_entry.is_completed = is_completed

    await session.flush()

    return log_entry
