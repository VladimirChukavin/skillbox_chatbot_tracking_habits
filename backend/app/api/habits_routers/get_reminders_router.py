import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.schemas.habit_schema import ReminderInfo
from app.services.habit_services.get_habits_by_reminder_service import (
    get_habits_by_reminder,
)

router = APIRouter()


@router.get("/internal/reminders", response_model=list[ReminderInfo])
async def get_reminders(
    time: str, session: AsyncSession = Depends(get_db_session)
) -> list[ReminderInfo]:
    try:
        hours, minutes = (int(part) for part in time.split(":"))
        reminder_time = datetime.time(hour=hours, minute=minutes)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="time должен быть в формате ЧЧ:ММ",
        )

    reminders = await get_habits_by_reminder(session, reminder_time)
    return [ReminderInfo(**rem) for rem in reminders]
