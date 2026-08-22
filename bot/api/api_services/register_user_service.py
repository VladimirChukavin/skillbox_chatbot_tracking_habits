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
