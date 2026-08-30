"""
Сервис для получения данных конкретной привычки через API бэкенда.

Содержит функцию для отправки GET-запроса на получение информации
о привычке с авторизацией пользователя.
"""

from requests import Session
from requests.exceptions import JSONDecodeError
from loguru import logger

from bot.api.api_services.authorized_request_service import _authorized_request


def get_habit_service(
    session: Session,
    base_url: str,
    telegram_id: int,
    habit_id: int,
) -> dict | None:
    """
    Получить данные привычки с бэкенда для указанного пользователя.

    Отправляет GET-запрос на эндпоинт /habits/{habit_id}.

    :param session: Сессия requests для переиспользования соединений
    :type session: Session
    :param base_url: Базовый URL API бэкенда
    :type base_url: str
    :param telegram_id: Telegram ID пользователя
    :type telegram_id: int
    :param habit_id: Идентификатор запрашиваемой привычки
    :type habit_id: int
    :return: Словарь с данными привычки или None при ошибке/отсутствии
    :rtype: dict | None
    """

    endpoint = f"/habits/{habit_id}"
    response = _authorized_request(session, base_url, "GET", telegram_id, endpoint)

    if response is None:
        logger.warning(
            "Нет ответа от сервера при получении привычки (habit_id={}, telegram_id={})",
            habit_id,
            telegram_id,
        )
        return None

    if response.ok:
        try:
            return response.json()
        except JSONDecodeError:
            logger.warning(
                "Сервер вернул успешный статус, но тело ответа не JSON (habit_id={}, telegram_id={}).",
                habit_id,
                telegram_id,
            )
            return None

    logger.warning(
        "Ошибка получения привычки (habit_id={}, telegram_id={}): status={} body={}",
        habit_id,
        telegram_id,
        response.status_code,
        response.text,
    )

    return None
