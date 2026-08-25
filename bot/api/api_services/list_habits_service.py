"""
Сервис для получения списка привычек пользователя через API бэкенда.

Содержит функцию для отправки GET-запроса на получение всех активных
привычек текущего пользователя.
"""

from requests import Session

from bot.api.api_services.authorized_request_service import _authorized_request


def list_habits_service(
    session: Session,
    base_url: str,
    method: str,
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
    :param method: HTTP-метод (ожидается "GET")
    :type method: str
    :param telegram_id: Telegram ID пользователя
    :type telegram_id: int
    :param endpoint: Путь эндпоинта (например, "/habits")
    :type endpoint: str
    :return: Список словарей с данными привычек (пустой список при ошибке)
    :rtype: list[dict]
    """

    response = _authorized_request(session, base_url, method, telegram_id, endpoint)

    if response is None:
        return []

    if response.status_code == 200:
        return response.json()

    return []
