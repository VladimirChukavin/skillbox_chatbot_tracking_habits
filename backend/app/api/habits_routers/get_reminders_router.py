"""
Роутер для получения привычек, требующих напоминания.

Обеспечивает внутренний endpoint для бота, который используется
планировщиком (APScheduler) каждую минуту для поиска привычек,
подлежащих уведомлению в заданное время.
"""

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
    """
    Получить список активных привычек для напоминания на указанное время.

    Принимает время в формате ЧЧ:ММ (UTC) в качестве query-параметра.
    Выполняет поиск в БД активных привычек, у которых часы и минуты
    reminder_time совпадают с переданным значением.

    :param time: Время напоминания в формате ЧЧ:ММ (UTC)
    :type time: str
    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :raises HTTPException: 422 — если параметр time не соответствует формату ЧЧ:ММ
    :return: Список объектов ReminderInfo
    :rtype: list[ReminderInfo]
    """

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
