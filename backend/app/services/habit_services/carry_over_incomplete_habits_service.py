"""
Сервис для автоматического переноса невыполненных привычек.

Содержит функцию, которая запускается по расписанию в конце дня
для создания записей о невыполнении активных привычек.
"""

import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_model import Habit
from app.models.habit_log_model import HabitLog


async def carry_over_incomplete_habits(session: AsyncSession) -> int:
    """
    Перенести невыполненные за сегодня привычки на следующий день.

    Находит все активные привычки, по которым нет отметки о выполнении
    за текущий день. Для каждой такой привычки:
    - Деактивирует её, если цель достигнута (completed_count >= target_days).
    - Создаёт запись в логе с is_completed=False, если лога за сегодня нет.

    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :return: Количество созданных записей о невыполнении
    :rtype: int
    """

    today = datetime.date.today()
    carried_count = 0

    completed_today_subquery = select(HabitLog.habit_id).where(
        HabitLog.log_date == today, HabitLog.is_completed.is_(True)
    )

    statement = (
        select(Habit)
        .where(Habit.is_active.is_(True))
        .where(~Habit.id.in_(completed_today_subquery))
    )

    result = await session.execute(statement)

    for habit in result.scalars():
        if habit.completed_count >= habit.target_days:
            habit.is_active = False
            continue

        existing_log = await session.execute(
            select(HabitLog).where(
                HabitLog.habit_id == habit.id, HabitLog.log_date == today
            )
        )

        if existing_log.scalar_one_or_none() is None:
            session.add(HabitLog(habit_id=habit.id, log_date=today, is_completed=False))
            carried_count += 1

    await session.flush()

    return carried_count
