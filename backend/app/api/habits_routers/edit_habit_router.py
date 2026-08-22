from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.database import get_db_session
from app.models.user_model import User
from app.schemas.habit_schema import HabitUpdate, HabitRead
from app.services.habit_services.get_habit_by_id_service import get_habit_by_id
from app.services.habit_services.update_habit_service import update_habit

router = APIRouter()


@router.patch("/{habit_id}", response_model=HabitRead)
async def edit_habit(
    habit_id: int,
    payload: HabitUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> HabitRead:
    habit = await get_habit_by_id(session, habit_id, current_user.id)

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Привычка не найдена",
        )

    updated = await update_habit(session, habit, payload, current_user)

    return HabitRead.model_validate(updated)
