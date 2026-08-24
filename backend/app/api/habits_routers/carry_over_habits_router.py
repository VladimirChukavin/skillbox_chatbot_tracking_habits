"""
Роутер для автоматического переноса невыполненных привычек.

Обеспечивает внутренний endpoint для ежедневного переноса привычек,
которые не были отмечены как выполненные, на следующий день.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.services.habit_services.carry_over_incomplete_habits_service import (
    carry_over_incomplete_habits,
)

router = APIRouter()


@router.post("/internal/carry-over", status_code=status.HTTP_200_OK)
async def carry_over_habits(session: AsyncSession = Depends(get_db_session)) -> dict:
    """
    Перенести невыполненные привычки на следующий день.

    Запускается планировщиком (APScheduler) в конце дня (23:59 UTC).
    Проверяет все активные привычки: если за текущий день нет отметки
    о выполнении, создаётся запись с is_completed=False.
    Привычки, достигшие цели (completed_count >= target_days),
    деактивируются (is_active=False).

    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :return: Словарь с количеством перенесённых привычек
    :rtype: dict
    """

    carried_count = await carry_over_incomplete_habits(session)
    return {"carried_count": carried_count}
