"""
Сервис для регистрации нового пользователя через API бэкенда.

Содержит функцию для отправки POST-запроса на создание учётной записи
и сохранения полученных JWT-токенов в хранилище.
"""

from typing import Any

from requests import Session
from loguru import logger

from bot.api.api_services.store_tokens_service import _store_tokens
from bot.config import BotSettings


def register_user_service(
    session: Session,
    base_url: str,
    bot_settings: BotSettings,
    telegram_id: int,
    full_name: str,
    password: str,
    username: str | None,
) -> dict[str, Any] | None:
    """
    Зарегистрировать пользователя на бэкенде.

    Отправляет данные пользователя (Telegram ID, имя, пароль, username)
    на эндпоинт /auth/register. При успешном ответе (статус 201)
    сохраняет полученные токены через _store_tokens.

    :param session: Сессия requests для переиспользования соединений
    :type session: Session
    :param base_url: Базовый URL API бэкенда
    :type base_url: str
    :param bot_settings: Объект настроек бота (для получения таймаута)
    :type bot_settings: BotSettings
    :param telegram_id: Telegram ID пользователя
    :type telegram_id: int
    :param full_name: Полное имя пользователя
    :type full_name: str
    :param password: Пароль пользователя
    :type password: str
    :param username: Username пользователя в Telegram (может быть None)
    :type username: str | None
    :return: Словарь с токенами при успехе, иначе None
    :rtype: dict[str, Any] | None
    """

    response = session.post(
        f"{base_url}/auth/register",
        json={
            "telegram_id": telegram_id,
            "full_name": full_name,
            "password": password,
            "username": username,
        },
        timeout=bot_settings.request_timeout,
    )

    if response.status_code == 201:
        _store_tokens(telegram_id, response.json())
        return response.json()

    logger.warning("Регистрация не удалась: {} {}", response.status_code, response.text)

    return None
