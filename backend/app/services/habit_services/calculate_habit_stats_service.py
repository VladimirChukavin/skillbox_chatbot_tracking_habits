import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_model import Habit
from app.models.habit_log_model import HabitLog


async def calculate_habit_stats(habit: Habit, session: AsyncSession) -> dict:
    today = datetime.date.today()
    today_log = await session.execute(
        select(HabitLog).where(
            HabitLog.habit_id == habit.id, HabitLog.log_date == today
        )
    )
    log_entry = today_log.scalar_one_or_none()
    is_completed_today = log_entry is not None and log_entry.is_completed

    progress = (
        (habit.completed_count / habit.target_days) * 100
        if habit.target_days > 0
        else 0
    )
    progress_percent = round(progress, 2)

    return {
        "habit_id": habit.id,
        "title": habit.title,
        "completed_count": habit.completed_count,
        "target_days": habit.target_days,
        "progress_percent": progress_percent,
        "is_completed_today": is_completed_today,
    }
