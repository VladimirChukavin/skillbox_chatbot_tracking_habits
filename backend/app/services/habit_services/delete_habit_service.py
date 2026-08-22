from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_model import Habit


async def delete_habit(session: AsyncSession, habit: Habit) -> None:
    await session.delete(habit)
    await session.flush()
