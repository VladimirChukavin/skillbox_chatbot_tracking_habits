from requests import Session

from bot.api.api_services.authorized_request_service import _authorized_request


def list_habits_service(
    session: Session,
    base_url: str,
    method: str,
    telegram_id: int,
    endpoint: str,
) -> list[dict]:
    response = _authorized_request(session, base_url, method, telegram_id, endpoint)

    if response is None:
        return []

    if response.status_code == 200:
        return response.json()

    return []
