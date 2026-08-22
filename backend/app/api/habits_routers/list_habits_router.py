from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.database import get_db_session
from app.models.user_model import User
from app.schemas.habit_schema import HabitRead
from app.services.habit_services.get_habits_by_user_service import get_habits_by_user

router = APIRouter()


@router.get("/", response_model=list[HabitRead])
async def list_habits(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> list[HabitRead]:
    habits = await get_habits_by_user(session, current_user.id)
    return [HabitRead.model_validate(hab) for hab in habits]
