from requests import Session

from bot.api.api_services.authorized_request_service import _authorized_request


def get_habit_stats_service(
    session: Session, base_url: str, method: str, telegram_id: int, habit_id: int
) -> dict | None:
    endpoint = f"/habits/{habit_id}/stats"
    response = _authorized_request(
        session,
        base_url,
        method,
        telegram_id,
        endpoint,
    )

    return response.json() if response and response.status_code == 200 else None
