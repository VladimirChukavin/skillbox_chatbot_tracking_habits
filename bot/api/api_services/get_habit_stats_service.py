"""
Сервис для получения статистики по привычке через API бэкенда.

Содержит функцию для отправки GET-запроса на получение прогресса
выполнения конкретной привычки с авторизацией пользователя.
"""

from requests import Session

from bot.api.api_services.authorized_request_service import _authorized_request


def get_habit_stats_service(
    session: Session, base_url: str, method: str, telegram_id: int, habit_id: int
) -> dict | None:
    """
    Получить статистику выполнения привычки с бэкенда.

    Отправляет GET-запрос на эндпоинт /habits/{habit_id}/stats.

    :param session: Сессия requests для переиспользования соединений
    :type session: Session
    :param base_url: Базовый URL API бэкенда
    :type base_url: str
    :param method: HTTP-метод (ожидается "GET")
    :type method: str
    :param telegram_id: Telegram ID пользователя
    :type telegram_id: int
    :param habit_id: Идентификатор привычки
    :type habit_id: int
    :return: Словарь со статистикой или None при ошибке/отсутствии
    :rtype: dict | None
    """

    endpoint = f"/habits/{habit_id}/stats"
    response = _authorized_request(
        session,
        base_url,
        method,
        telegram_id,
        endpoint,
    )

    return response.json() if response and response.status_code == 200 else None
