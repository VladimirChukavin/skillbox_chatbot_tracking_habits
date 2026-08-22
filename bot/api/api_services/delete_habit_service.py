from requests import Session

from bot.api.api_services.authorized_request_service import _authorized_request


def delete_habit_service(
    session: Session,
    base_url: str,
    method: str,
    telegram_id: int,
    habit_id: int,
) -> bool:
    endpoint = f"/habits/{habit_id}"
    response = _authorized_request(session, base_url, method, telegram_id, endpoint)

    return response is not None and response.status_code == 204
