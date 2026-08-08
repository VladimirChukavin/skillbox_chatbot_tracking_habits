from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.deps import get_current_user
from backend.app.database import get_db_session
from backend.app.models.user_model import User
from backend.app.schemas.habit_schema import (
    HabitCreate,
    HabitUpdate,
    HabitRead,
    HabitStats,
    HabitTrackRequest,
)
from backend.app.services.habit_service import (
    calculate_habit_stats,
    create_habit,
    delete_habit,
    get_habit_by_id,
    get_habits_by_user,
    track_habit,
    update_habit,
)

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post("/", response_model=HabitRead, status_code=status.HTTP_201_CREATED)
async def create_new_habit(
    payload: HabitCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> HabitRead:
    habit = await create_habit(session, current_user.id, payload)
    return HabitRead.model_validate(habit)


@router.get("/", response_model=list[HabitRead])
async def list_habits(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> list[HabitRead]:
    habits = await get_habits_by_user(session, current_user.id)
    return [HabitRead.model_validate(hab) for hab in habits]


@router.get("/{habit_id}", response_model=HabitRead)
async def retrieve_habit(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> HabitRead:
    habit = await get_habit_by_id(session, habit_id, current_user.id)

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Привычка не найдена",
        )

    return HabitRead.model_validate(habit)


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

    updated = await update_habit(session, habit, payload)

    return HabitRead.model_validate(updated)


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_habit(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> None:
    habit = await get_habit_by_id(session, habit_id, current_user.id)

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Привычка не найдена",
        )

    await delete_habit(session, habit)


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


@router.get("/{habit_id}/stats", response_model=HabitStats)
async def get_habit_stats(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> HabitStats:
    habit = await get_habit_by_id(session, habit_id, current_user.id)

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Привычка не найдена"
        )

    stats = await calculate_habit_stats(habit, session)

    return HabitStats(**stats)
