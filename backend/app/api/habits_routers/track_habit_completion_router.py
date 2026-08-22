from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.database import get_db_session
from app.models.user_model import User
from app.schemas.habit_schema import HabitRead, HabitTrackRequest
from app.services.habit_services.get_habit_by_id_service import get_habit_by_id
from app.services.habit_services.track_habit_service import track_habit

router = APIRouter()


@router.post("/{habit_id}/track", response_model=HabitRead)
async def track_habit_completion(
    habit_id: int,
    payload: HabitTrackRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> HabitRead:
    habit = await get_habit_by_id(session, habit_id, current_user.id)

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Привычка не найдена"
        )

    await track_habit(session, habit, payload.is_completed, payload.log_date)

    return HabitRead.model_validate(habit)
