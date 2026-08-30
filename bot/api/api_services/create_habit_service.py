"""
Сервис для создания новой привычки через API бэкенда.

Содержит функцию для отправки POST-запроса на создание привычки
с авторизацией пользователя.
"""

from requests import Session
from requests.exceptions import JSONDecodeError
from loguru import logger

from bot.api.api_services.authorized_request_service import _authorized_request


def create_habit_service(
    session: Session,
    base_url: str,
    telegram_id: int,
    habit_data: dict,
) -> dict | None:
    """
    Создать привычку на бэкенде для указанного пользователя.

    Отправляет данные привычки в формате JSON на эндпоинт /habits.

    :param session: Сессия requests для переиспользования соединений
    :type session: Session
    :param base_url: Базовый URL API бэкенда
    :type base_url: str
    :param telegram_id: Telegram ID пользователя
    :type telegram_id: int
    :param habit_data: Словарь с данными привычки (title, description, и т.д.)
    :type habit_data: dict
    :return: Словарь с данными созданной привычки или None при ошибке
    :rtype: dict | None
    """

    response = _authorized_request(
        session,
        base_url,
        "POST",
        telegram_id,
        "/habits",
        json=habit_data,
    )

    if response is None:
        logger.warning(
            "Нет ответа от сервера при создании привычки (telegram_id={})",
            telegram_id,
        )
        return None

    if response.ok:
        try:
            return response.json()
        except JSONDecodeError:
            logger.warning(
                "Сервер вернул успешный статус, но тело ответа не JSON (telegram_id={}). Статус {}",
                telegram_id,
                response.status_code,
            )
            return None

    logger.warning(
        "Ошибка создания привычки (telegram_id={}): status={} body={}",
        telegram_id,
        response.status_code,
        response.text,
    )

    return {"error": response.text}
