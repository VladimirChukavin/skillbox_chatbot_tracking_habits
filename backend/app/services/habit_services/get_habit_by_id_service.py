from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_model import Habit


async def get_habit_by_id(
    session: AsyncSession, habit_id: int, user_id: int
) -> Habit | None:
    result = await session.execute(
        select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    )

    return result.scalar_one_or_none()
