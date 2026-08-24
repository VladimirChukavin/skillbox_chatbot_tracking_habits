"""
Роутер для получения информации о конкретной привычке.

Обеспечивает endpoint для просмотра детальной информации об отдельной
привычке текущего пользователя.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.database import get_db_session
from app.models.user_model import User
from app.schemas.habit_schema import HabitRead
from app.services.habit_services.get_habit_by_id_service import get_habit_by_id

router = APIRouter()


@router.get("/{habit_id}", response_model=HabitRead)
async def retrieve_habit(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> HabitRead:
    """
    Получить информацию о конкретной привычке пользователя.

    Ищет привычку по её ID, проверяя принадлежность текущему пользователю.

    :param habit_id: ID запрашиваемой привычки
    :type habit_id: int
    :param current_user: Текущий авторизованный пользователь
    :type current_user: User
    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :raises HTTPException: 404 — если привычка не найдена или не принадлежит пользователю
    :return: Данные запрошенной привычки
    :rtype: HabitRead
    """

    habit = await get_habit_by_id(session, habit_id, current_user.id)

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Привычка не найдена",
        )

    return HabitRead.model_validate(habit)
