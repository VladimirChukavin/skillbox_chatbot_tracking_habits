"""
Сервис для получения данных конкретной привычки через API бэкенда.

Содержит функцию для отправки GET-запроса на получение информации
о привычке с авторизацией пользователя.
"""

from requests import Session

from bot.api.api_services.authorized_request_service import _authorized_request


def get_habit_service(
    session: Session,
    base_url: str,
    method: str,
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
    :param method: HTTP-метод (ожидается "GET")
    :type method: str
    :param telegram_id: Telegram ID пользователя
    :type telegram_id: int
    :param habit_id: Идентификатор запрашиваемой привычки
    :type habit_id: int
    :return: Словарь с данными привычки или None при ошибке/отсутствии
    :rtype: dict | None
    """

    endpoint = f"/habits/{habit_id}"
    response = _authorized_request(session, base_url, method, telegram_id, endpoint)

    return response.json() if response and response.status_code == 200 else None
