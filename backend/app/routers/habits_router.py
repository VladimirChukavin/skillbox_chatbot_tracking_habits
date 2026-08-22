import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.database import get_db_session
from app.models.user_model import User
from app.schemas.habit_schema import (
    HabitCreate,
    HabitUpdate,
    HabitRead,
    HabitStats,
    HabitTrackRequest,
    ReminderInfo,
)
from app.services.habit_service import (
    calculate_habit_stats,
    create_habit,
    delete_habit,
    get_habit_by_id,
    get_habits_by_user,
    track_habit,
    update_habit,
    carry_over_incomplete_habits,
    get_habits_by_reminder,
)

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post("", response_model=HabitRead, status_code=status.HTTP_201_CREATED)
async def create_new_habit(
    payload: HabitCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> HabitRead:
    habit = await create_habit(session, current_user.id, payload, current_user)
    return HabitRead.model_validate(habit)


@router.get("", response_model=list[HabitRead])
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

    updated = await update_habit(session, habit, payload, current_user)

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


@router.post("/internal/carry-over", status_code=status.HTTP_200_OK)
async def carry_over_habits(session: AsyncSession = Depends(get_db_session)) -> dict:
    carried_count = await carry_over_incomplete_habits(session)
    return {"carried_count": carried_count}


@router.get("/internal/reminders", response_model=list[ReminderInfo])
async def get_reminders(
    time: str, session: AsyncSession = Depends(get_db_session)
) -> list[ReminderInfo]:
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
