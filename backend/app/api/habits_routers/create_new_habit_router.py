from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.database import get_db_session
from app.models.user_model import User
from app.schemas.habit_schema import HabitCreate, HabitRead
from app.services.habit_services.create_habit_service import create_habit

router = APIRouter()


@router.post("/", response_model=HabitRead, status_code=status.HTTP_201_CREATED)
async def create_new_habit(
    payload: HabitCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> HabitRead:
    habit = await create_habit(session, current_user.id, payload, current_user)
    return HabitRead.model_validate(habit)
