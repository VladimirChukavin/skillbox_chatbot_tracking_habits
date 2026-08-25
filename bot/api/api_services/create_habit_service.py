"""
Сервис для создания новой привычки через API бэкенда.

Содержит функцию для отправки POST-запроса на создание привычки
с авторизацией пользователя.
"""

from requests import Session

from bot.api.api_services.authorized_request_service import _authorized_request


def create_habit_service(
    session: Session,
    base_url: str,
    method: str,
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
    :param method: HTTP-метод (ожидается "POST")
    :type method: str
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
        method,
        telegram_id,
        "/habits",
        json=habit_data,
    )

    return response.json() if response and response.status_code == 201 else None
