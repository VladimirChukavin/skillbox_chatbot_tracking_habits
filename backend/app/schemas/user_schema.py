import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    telegram_id: int
    full_name: str = Field(min_length=1, max_length=255)
    username: str | None = None
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    telegram_id: int
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: int
    full_name: str
    username: str | None
    timezone: str
    created_at: datetime.datetime
