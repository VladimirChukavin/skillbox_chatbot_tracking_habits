from typing import Any

from requests import Session
from loguru import logger

from bot.api.api_services.store_tokens_service import _store_tokens
from bot.config import BotSettings


def login_user_service(
    session: Session,
    base_url: str,
    bot_settings: BotSettings,
    telegram_id: int,
    password: str,
) -> dict[str, Any] | None:
    response = session.post(
        f"{base_url}/auth/login",
        json={
            "telegram_id": telegram_id,
            "password": password,
        },
        timeout=bot_settings.request_timeout,
    )

    if response.status_code == 200:
        _store_tokens(telegram_id, response.json())
        return response.json()

    logger.warning("Логин не удался: {} {}", response.status_code, response.text)

    return None
