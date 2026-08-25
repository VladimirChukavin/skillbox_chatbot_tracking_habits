"""
Сервис для отметки выполнения привычки через API бэкенда.

Содержит функцию для отправки POST-запроса на фиксацию факта
выполнения или невыполнения привычки за текущий день.
"""

from requests import Session

from bot.api.api_services.authorized_request_service import _authorized_request


def track_habit_service(
    session: Session,
    base_url: str,
    method: str,
    telegram_id: int,
    habit_id: int,
    is_completed: bool,
) -> dict | None:
    """
    Отправить отметку о выполнении привычки на бэкенд.

    Отправляет POST-запрос на эндпоинт /habits/{habit_id}/track
    с указанием статуса выполнения.

    :param session: Сессия requests для переиспользования соединений
    :type session: Session
    :param base_url: Базовый URL API бэкенда
    :type base_url: str
    :param method: HTTP-метод (ожидается "POST")
    :type method: str
    :param telegram_id: Telegram ID пользователя
    :type telegram_id: int
    :param habit_id: Идентификатор привычки
    :type habit_id: int
    :param is_completed: Статус выполнения (True — выполнено, False — нет)
    :type is_completed: bool
    :return: Словарь с обновлёнными данными привычки или None при ошибке
    :rtype: dict | None
    """

    endpoint = f"/habits/{habit_id}/track"
    response = _authorized_request(
        session,
        base_url,
        method,
        telegram_id,
        endpoint,
        json={"is_completed": is_completed},
    )

    return response.json() if response and response.status_code == 200 else None
