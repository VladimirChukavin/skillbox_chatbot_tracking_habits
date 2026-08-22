import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_model import Habit
from app.models.habit_log_model import HabitLog


async def carry_over_incomplete_habits(session: AsyncSession) -> int:
    today = datetime.date.today()
    carried_count = 0

    completed_today_subquery = (
        select(HabitLog.habit_id).where(
            HabitLog.log_date == today, HabitLog.is_completed.is_(True)
        )
    ).subquery()

    statement = (
        select(Habit)
        .where(Habit.is_active.is_(True))
        .where(~Habit.id.in_(completed_today_subquery.c.habit_id))
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
