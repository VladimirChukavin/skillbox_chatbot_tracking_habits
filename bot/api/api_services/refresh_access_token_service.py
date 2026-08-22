from requests import Session

from bot.api.api_services.store_tokens_service import _store_tokens
from bot.config import bot_settings
from bot.storage import token_storage


def _refresh_access_token(telegram_id: int, session: Session, base_url: str) -> bool:
    bundle = token_storage.get_tokens(telegram_id)

    if bundle is None:
        return False

    response = session.post(
        f"{base_url}/auth/refresh",
        params={"refresh_token": bundle.refresh_token},
        timeout=bot_settings.request_timeout,
    )

    if response.status_code == 200:
        _store_tokens(telegram_id, response.json())
        return True

    token_storage.clear_tokens(telegram_id)

    return False
