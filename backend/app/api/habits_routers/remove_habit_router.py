"""
Роутер для удаления привычки.

Обеспечивает endpoint для полного удаления привычки текущего пользователя
из базы данных.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.database import get_db_session
from app.models.user_model import User
from app.services.habit_services.delete_habit_service import delete_habit
from app.services.habit_services.get_habit_by_id_service import get_habit_by_id

router = APIRouter()


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_habit(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> None:
    """
    Удалить привычку текущего пользователя.

    Безвозвратно удаляет привычку и все связанные с ней логи выполнения
    (благодаря каскадному удалению на уровне БД). Перед удалением проверяет
    принадлежность привычки текущему пользователю.

    :param habit_id: ID удаляемой привычки
    :type habit_id: int
    :param current_user: Текущий авторизованный пользователь
    :type current_user: User
    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :raises HTTPException: 404 — если привычка не найдена или не принадлежит пользователю
    :return: Ничего не возвращает (статус 204 No Content)
    :rtype: None
    """

    habit = await get_habit_by_id(session, habit_id, current_user.id)

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Привычка не найдена",
        )

    await delete_habit(session, habit)
