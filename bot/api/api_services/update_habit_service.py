"""
Сервис для обновления данных привычки через API бэкенда.

Содержит функцию для отправки PATCH-запроса на частичное обновление
информации о привычке с авторизацией пользователя.
"""

from requests import Session
from requests.exceptions import JSONDecodeError
from loguru import logger

from bot.api.api_services.authorized_request_service import _authorized_request


def update_habit_service(
    session: Session,
    base_url: str,
    telegram_id: int,
    habit_id: int,
    habit_data: dict,
) -> dict | None:
    """
    Обновить данные привычки на бэкенде.

    Отправляет PATCH-запрос на эндпоинт /habits/{habit_id} с новыми
    данными привычки в формате JSON.

    :param session: Сессия requests для переиспользования соединений
    :type session: Session
    :param base_url: Базовый URL API бэкенда
    :type base_url: str
    :param telegram_id: Telegram ID пользователя
    :type telegram_id: int
    :param habit_id: Идентификатор обновляемой привычки
    :type habit_id: int
    :param habit_data: Словарь с полями привычки для обновления
    :type habit_data: dict
    :return: Словарь с обновлёнными данными привычки или None при ошибке
    :rtype: dict | None
    """

    endpoint = f"/habits/{habit_id}"
    response = _authorized_request(
        session,
        base_url,
        "PATCH",
        telegram_id,
        endpoint,
        json=habit_data,
    )

    if response is None:
        logger.warning(
            "Нет ответа от сервера при обновлении привычки (habit_id={}, telegram_id={})",
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
        "Ошибка обновления привычки (habit_id={}, telegram_id={}): status={} body={}",
        habit_id,
        telegram_id,
        response.status_code,
        response.text,
    )

    return None
