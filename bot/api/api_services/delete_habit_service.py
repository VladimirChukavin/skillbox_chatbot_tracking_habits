"""
Сервис для удаления привычки через API бэкенда.

Содержит функцию для отправки DELETE-запроса на удаление привычки
с авторизацией пользователя.
"""

from loguru import logger
from requests import Session

from bot.api.api_services.authorized_request_service import _authorized_request


def delete_habit_service(
    session: Session,
    base_url: str,
    telegram_id: int,
    habit_id: int,
) -> bool:
    """
    Удалить привычку на бэкенде для указанного пользователя.

    Отправляет DELETE-запрос на эндпоинт /habits/{habit_id}.

    :param session: Сессия requests для переиспользования соединений
    :type session: Session
    :param base_url: Базовый URL API бэкенда
    :type base_url: str
    :param telegram_id: Telegram ID пользователя
    :type telegram_id: int
    :param habit_id: Идентификатор удаляемой привычки
    :type habit_id: int
    :return: True, если удаление успешно (статус 204), иначе False
    :rtype: bool
    """

    endpoint = f"/habits/{habit_id}"
    response = _authorized_request(session, base_url, "DELETE", telegram_id, endpoint)

    if response is None:
        logger.warning(
            "Нет ответа от сервера при удалении привычки (habit_id={}, telegram_id={})",
            habit_id,
            telegram_id,
        )

    if response.ok:
        logger.info(
            "Привычка успешно удалена (habit_id={}, telegram_id={})",
            habit_id,
            telegram_id,
        )
        return True

    logger.warning(
        "Ошибка удаления привычки (habit_id={}, telegram_id={}): status={}, body={}",
        habit_id,
        telegram_id,
        response.status_code,
        response.text,
    )

    return False
