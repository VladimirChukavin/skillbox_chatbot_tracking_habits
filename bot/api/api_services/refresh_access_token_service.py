"""
Сервис для обновления access-токена через API бэкенда.

Содержит функцию для отправки refresh-токена на бэкенд с целью получения
новой пары JWT-токенов.
"""

from requests import Session
from requests.exceptions import RequestException, JSONDecodeError
from loguru import logger

from bot.api.api_services.store_tokens_service import _store_tokens
from bot.config import bot_settings
from bot.storage import token_storage


def _refresh_access_token(telegram_id: int, session: Session, base_url: str) -> bool:
    """
    Обновить access-токен, используя сохранённый refresh-токен.

    Отправляет refresh-токен как query-параметр на эндпоинт /auth/refresh.
    При успешном обновлении (статус 200) сохраняет новые токены.
    При неудаче (например, истёкший refresh-токен) очищает хранилище токенов
    пользователя, требуя повторный вход.

    :param telegram_id: Telegram ID пользователя
    :type telegram_id: int
    :param session: Сессия requests для переиспользования соединений
    :type session: Session
    :param base_url: Базовый URL API бэкенда
    :type base_url: str
    :return: True, если токены успешно обновлены, иначе False
    :rtype: bool
    """

    bundle = token_storage.get_tokens(telegram_id)

    if bundle is None:
        logger.warning("Нет токенов для обновления (telegram_id={})", telegram_id)
        return False

    try:
        response = session.post(
            f"{base_url}/auth/refresh",
            params={"refresh_token": bundle.refresh_token},
            timeout=bot_settings.request_timeout,
        )
    except RequestException as error:
        logger.error(
            "Сетевая ошибка при обновлении токена: (telegram_id={}): {}",
            telegram_id,
            str(error),
        )
        return False

    if response.ok:
        try:
            data = response.json()
        except JSONDecodeError:
            logger.warning(
                "Сервер вернул успешный статус, но тело ответа не JSON (telegram_id={})",
                telegram_id,
            )
            return False

        _store_tokens(telegram_id, data)
        return True

    logger.warning(
        "Ошибка обновления токена (telegram_id={}): status={} body={}",
        telegram_id,
        response.status_code,
        response.text,
    )

    token_storage.clear_tokens(telegram_id)

    return False
