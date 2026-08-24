"""
Pydantic-схемы для работы с JWT-токенами.

Содержит модели для представления полезной нагрузки (payload) токена
и связки access/refresh токенов для ответов API.
"""

from pydantic import BaseModel


class TokenPayload(BaseModel):
    """
    Схема полезной нагрузки (payload) JWT-токена.

    :param sub: Идентификатор пользователя (subject)
    :param telegram_id: Telegram ID пользователя
    :param exp: Срок действия токена
    :param type: Тип токена ("access" или "refresh")
    """

    sub: str
    telegram_id: int
    exp: int | None = None
    type: str = "access"


class TokenBundle(BaseModel):
    """
    Схема связки токенов (ответ API при логине/регистрации).

    :param access_token: Короткоживущий токен для доступа к API
    :param refresh_token: Долгоживущий токен для обновления access-токена
    :param token_type: Тип токена (всегда "bearer")
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
