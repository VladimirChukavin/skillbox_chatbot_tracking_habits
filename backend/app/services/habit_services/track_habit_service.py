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
