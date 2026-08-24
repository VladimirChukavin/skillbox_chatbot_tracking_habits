"""
Pydantic-схемы для валидации данных пользователей.

Содержит модели для регистрации, аутентификации и чтения профиля пользователя.
"""

import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """
    Схема для создания (регистрации) нового пользователя.

    :param telegram_id: Уникальный Telegram ID пользователя
    :param full_name: Полное имя пользователя (от 1 до 255 символов)
    :param username: Имя пользователя в Telegram (опционально)
    :param password: Пароль в открытом виде (от 6 до 128 символов)
    """

    telegram_id: int
    full_name: str = Field(min_length=1, max_length=255)
    username: str | None = None
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    """
    Схема для входа пользователя в систему.

    :param telegram_id: Telegram ID пользователя
    :param password: Пароль в открытом виде
    """

    telegram_id: int
    password: str


class UserRead(BaseModel):
    """
    Схема для чтения данных пользователя (ответ API).

    Исключает чувствительные данные, такие как хеш пароля и refresh-токен.

    :param id: Идентификатор пользователя в БД
    :param telegram_id: Telegram ID пользователя
    :param full_name: Полное имя пользователя
    :param username: Имя пользователя в Telegram
    :param timezone: Часовой пояс пользователя
    :param created_at: Дата и время регистрации
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: int
    full_name: str
    username: str | None
    timezone: str
    created_at: datetime.datetime
