"""
Сервис для получения списка привычек пользователя через API бэкенда.

Содержит функцию для отправки GET-запроса на получение всех активных
привычек текущего пользователя.
"""

from requests import Session
from requests.exceptions import JSONDecodeError
from loguru import logger

from bot.api.api_services.authorized_request_service import _authorized_request


def list_habits_service(
    session: Session,
    base_url: str,
    telegram_id: int,
    endpoint: str,
) -> list[dict]:
    """
    Получить список всех привычек пользователя с бэкенда.

    Отправляет GET-запрос на указанный эндпоинт /habits.
    В случае ошибки авторизации или соединения возвращает пустой список.

    :param session: Сессия requests для переиспользования соединений
    :type session: Session
    :param base_url: Базовый URL API бэкенда
    :type base_url: str
    :param telegram_id: Telegram ID пользователя
    :type telegram_id: int
    :param endpoint: Путь эндпоинта (например, "/habits")
    :type endpoint: str
    :return: Список словарей с данными привычек (пустой список при ошибке)
    :rtype: list[dict]
    """

    response = _authorized_request(session, base_url, "GET", telegram_id, endpoint)

    if response is None:
        logger.warning(
            "Нет ответа от сервера при получении списка привычек (telegram_id={}, endpoint={})",
            telegram_id,
            endpoint,
        )
        return []

    if response.ok:
        try:
            return response.json()
        except JSONDecodeError:
            logger.warning(
                "Сервер вернул успешный ответ, но тело ответа не JSON (telegram_id={}, endpoint={})",
                telegram_id,
                endpoint,
            )
            return []

    logger.warning(
        "Ошибка получения списка привычек (telegram_id={}, endpoint={}): status={} body={}",
        telegram_id,
        endpoint,
        response.status_code,
        response.text,
    )

    return []
