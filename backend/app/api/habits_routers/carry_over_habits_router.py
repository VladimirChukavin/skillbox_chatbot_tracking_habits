from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.services.habit_services.carry_over_incomplete_habits_service import (
    carry_over_incomplete_habits,
)

router = APIRouter()


@router.post("/internal/carry-over", status_code=status.HTTP_200_OK)
async def carry_over_habits(session: AsyncSession = Depends(get_db_session)) -> dict:
    carried_count = await carry_over_incomplete_habits(session)
    return {"carried_count": carried_count}
