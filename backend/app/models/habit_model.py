"""
Модель SQLAlchemy для привычек пользователя.

Описывает таблицу habits, которая хранит информацию о привычках,
их целях, прогрессе выполнения и времени напоминаний.
"""

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.habit_log_model import HabitLog
    from app.models.user_model import User


class Habit(Base):
    """
    Модель привычки пользователя.

    Содержит настройки привычки (название, цель, срок) и данные о её
    выполнении (счётчик выполненных дней, статус активности).

    :param id: Первичный ключ
    :param user_id: ID пользователя (внешний ключ на users.id)
    :param title: Название привычки
    :param description: Описание привычки (опционально)
    :param target_description: Цель привычки (опционально)
    :param target_days: Целевое количество дней для выполнения (по умолчанию 21)
    :param completed_count: Текущее количество выполненных дней
    :param is_active: Статус активности привычки (по умолчанию True)
    :param reminder_time: Время напоминания в UTC (опционально)
    :param created_at: Дата и время создания привычки
    :param user: Объект связанной модели User
    :param logs: Список объектов связанных логов выполнения HabitLog
    """

    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_days: Mapped[int] = mapped_column(
        Integer, default=21, server_default=text("21"), nullable=False
    )
    completed_count: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true"), nullable=False
    )
    reminder_time: Mapped[datetime.time | None] = mapped_column(Time, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="habits")
    logs: Mapped[list["HabitLog"]] = relationship(
        "HabitLog", back_populates="habit", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта привычки.

        :return: Форматированная строка с названием привычки
        :rtype: str
        """

        return f"Habit(title={self.title})"
