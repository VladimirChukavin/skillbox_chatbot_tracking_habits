import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.habit_model import Habit
from app.models.habit_log_model import HabitLog
from app.schemas.habit_schema import HabitCreate, HabitUpdate

settings = get_settings()


async def create_habit(
    session: AsyncSession, user_id: int, payload: HabitCreate
) -> Habit:
    habit = Habit(
        user_id=user_id,
        title=payload.title,
        description=payload.description,
        target_description=payload.target_description,
        target_days=payload.target_days,
        reminder_time=payload.reminder_time,
    )
    session.add(habit)
    await session.flush()

    return habit


async def get_habits_by_user(
    session: AsyncSession, user_id: int, active_only: bool = True
) -> list[Habit]:
    statement = select(Habit).where(Habit.user_id == user_id)

    if active_only:
        statement = statement.where(Habit.is_active.is_(True))

    statement = statement.order_by(Habit.created_at.desc())
    result = await session.execute(statement)

    return list(result.scalars().all())


async def get_habit_by_id(
    session: AsyncSession, habit_id: int, user_id: int
) -> Habit | None:
    result = await session.execute(
        select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    )

    return result.scalar_one_or_none()


async def update_habit(
    session: AsyncSession, habit: Habit, payload: HabitUpdate
) -> Habit:
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(habit, field, value)

    await session.flush()

    return habit


async def delete_habit(session: AsyncSession, habit: Habit) -> None:
    await session.delete(habit)
    await session.flush()


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
