"""
Модель SQLAlchemy для пользователей.

Описывает таблицу users, которая хранит учётные данные пользователей,
их часовые пояса и refresh-токены для авторизации.
"""

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.habit_model import Habit


class User(Base):
    """
    Модель пользователя приложения.

    :param id: Первичный ключ
    :param telegram_id: Уникальный Telegram ID пользователя
    :param username: Имя пользователя в Telegram (опционально)
    :param full_name: Полное имя пользователя
    :param hashed_password: Хешированный пароль
    :param timezone: Часовой пояс пользователя (по умолчанию "UTC")
    :param refresh_token: JWT refresh-токен для обновления access-токена (опционально)
    :param created_at: Дата и время регистрации пользователя
    :param habits: Список объектов связанных привычек Habit
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="UTC", nullable=False)
    refresh_token: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    habits: Mapped[list["Habit"]] = relationship(
        "Habit", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта пользователя.

        :return: Форматированная строка с username и полным именем
        :rtype: str
        """

        return f"User(username={self.username}, full_name={self.full_name})"
