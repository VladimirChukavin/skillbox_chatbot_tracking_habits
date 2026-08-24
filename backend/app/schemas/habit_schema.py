"""
Pydantic-схемы для валидации данных привычек.

Содержит модели для создания, обновления, чтения привычек,
отметки выполнения и получения статистики.
"""

import datetime

from pydantic import BaseModel, ConfigDict, Field


class HabitBase(BaseModel):
    """
    Базовая схема привычки с общими полями.

    :param title: Название привычки (от 1 до 255 символов)
    :param description: Описание привычки (опционально)
    :param target_description: Цель привычки (опционально)
    :param target_days: Целевое количество дней (от 1 до 365, по умолчанию 21)
    """

    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    target_description: str | None = None
    target_days: int = Field(default=21, ge=1, le=365)


class HabitCreate(HabitBase):
    """
    Схема для создания новой привычки.

    :param reminder_time: Время напоминания в локальном часовом поясе (опционально)
    """

    reminder_time: datetime.time | None = None


class HabitUpdate(BaseModel):
    """
    Схема для частичного обновления привычки.

    Все поля опциональны — обновляются только переданные значения.

    :param title: Название привычки (от 1 до 255 символов)
    :param description: Описание привычки (опционально)
    :param target_description: Цель привычки (опционально)
    :param target_days: Целевое количество дней (от 1 до 365)
    :param reminder_time: Время напоминания в локальном часовом поясе (опционально)
    :param is_active: Статус активности привычки (опционально)
    """

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    target_description: str | None = None
    target_days: int | None = Field(default=None, ge=1, le=365)
    reminder_time: datetime.time | None = None
    is_active: bool | None = None


class HabitRead(HabitBase):
    """
    Схема для чтения данных привычки (ответ API).

    :param id: Идентификатор привычки
    :param completed_count: Количество выполненных дней
    :param is_active: Статус активности
    :param reminder_time: Время напоминания (в UTC)
    :param created_at: Дата и время создания
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    completed_count: int
    is_active: bool
    reminder_time: datetime.time | None
    created_at: datetime.datetime


class HabitTrackRequest(BaseModel):
    """
    Схема запроса для отметки выполнения привычки.

    :param is_completed: Статус выполнения (True/False)
    :param log_date: Дата отметки (по умолчанию текущий день)
    """

    is_completed: bool
    log_date: datetime.date | None = None


class HabitStats(BaseModel):
    """
    Схема статистики выполнения привычки.

    :param habit_id: Идентификатор привычки
    :param title: Название привычки
    :param completed_count: Количество выполненных дней
    :param target_days: Целевое количество дней
    :param progress_percent: Процент выполнения (0-100)
    :param is_completed_today: Выполнена ли привычка сегодня
    """

    habit_id: int
    title: str
    completed_count: int
    target_days: int
    progress_percent: float
    is_completed_today: bool


class ReminderInfo(BaseModel):
    """
    Схема информации о напоминании для внутреннего API.

    :param telegram_id: Telegram ID пользователя для отправки уведомления
    :param habit_id: Идентификатор привычки
    :param title: Название привычки для текста уведомления
    """

    telegram_id: int
    habit_id: int
    title: str
