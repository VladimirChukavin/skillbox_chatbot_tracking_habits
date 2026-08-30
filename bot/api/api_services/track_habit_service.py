"""
Сервис для отметки выполнения привычки через API бэкенда.

Содержит функцию для отправки POST-запроса на фиксацию факта
выполнения или невыполнения привычки за текущий день.
"""

from requests import Session
from requests.exceptions import JSONDecodeError
from loguru import logger

from bot.api.api_services.authorized_request_service import _authorized_request


def track_habit_service(
    session: Session,
    base_url: str,
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
        "POST",
        telegram_id,
        endpoint,
        json={"is_completed": is_completed},
    )

    if response is None:
        logger.warning(
            "Нет ответа от сервера при отметке привычки (habit_id={}, telegram_id={})",
            habit_id,
            telegram_id,
        )
        return None

    if response.ok:
        try:
            return response.json()
        except JSONDecodeError:
            logger.warning(
                "Сервер вернул успешный статус, но тело ответа не JSON (habit_id={}, telegram_id={})",
                habit_id,
                telegram_id,
            )
            return None

    logger.warning(
        "Ошибка отметки привычки (habit_id={}, telegram_id={}): status={} body={}",
        habit_id,
        telegram_id,
        response.status_code,
        response.text,
    )

    return None
