from requests import Session

from bot.api.api_services.authorized_request_service import _authorized_request


def update_habit_service(
    session: Session,
    base_url: str,
    method: str,
    telegram_id: int,
    habit_id: int,
    habit_data: dict,
) -> dict | None:
    endpoint = f"/habits/{habit_id}"
    response = _authorized_request(
        session,
        base_url,
        method,
        telegram_id,
        endpoint,
        json=habit_data,
    )

    return response.json() if response and response.status_code == 200 else None
