import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_model import Habit
from app.models import User
from app.schemas.habit_schema import HabitUpdate


async def update_habit(
    session: AsyncSession, habit: Habit, payload: HabitUpdate, user: User
) -> Habit:
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
