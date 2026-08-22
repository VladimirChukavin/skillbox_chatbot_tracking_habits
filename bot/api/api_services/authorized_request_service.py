from typing import Any

from requests import Response, Session
from loguru import logger

from bot.api.api_services.refresh_access_token_service import _refresh_access_token
from bot.config import bot_settings
from bot.storage import token_storage


def _authorized_request(
    session: Session,
    base_url: str,
    method: str,
    telegram_id: int,
    endpoint: str,
    **kwargs: Any,
) -> Response | None:
    bundle = token_storage.get_tokens(telegram_id)

    if bundle is None:
        logger.warning("Нет сохраненных токенов для telegram_id={}", telegram_id)
        return None

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {bundle.access_token}"

    response = session.request(
        method,
        f"{base_url}{endpoint}",
        headers=headers,
        timeout=bot_settings.request_timeout,
        **kwargs,
    )

    if response.status_code == 401:
        if _refresh_access_token(telegram_id, session, base_url):
            bundle = token_storage.get_tokens(telegram_id)
            headers["Authorization"] = f"Bearer {bundle.access_token}"
            response = session.request(
                method,
                f"{base_url}{endpoint}",
                headers=headers,
                timeout=bot_settings.request_timeout,
                **kwargs,
            )

    return response
