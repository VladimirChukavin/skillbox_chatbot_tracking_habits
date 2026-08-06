import datetime

from pydantic import BaseModel, ConfigDict, Field


class HabitBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    target_description: str | None = None
    target_days: int = Field(default=21, ge=1, le=365)


class HabitCreate(HabitBase):
    reminder_time: datetime.time | None = None


class HabitUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    target_description: str | None = None
    target_days: int | None = Field(default=None, ge=1, le=365)
    reminder_time: datetime.time | None = None
    is_active: bool | None = None


class HabitRead(HabitBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    completed_count: int
    is_active: bool
    reminder_time: datetime.time | None
    created_at: datetime.datetime


class HabitTrackRequest(BaseModel):
    is_completed: bool
    log_date: datetime.datetime | None = None


class HabitStats(BaseModel):
    habit_id: int
    title: str
    completed_count: int
    target_days: int
    progress_percent: float
    is_completed_today: bool
