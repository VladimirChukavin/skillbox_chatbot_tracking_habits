"""
Сервис для выполнения авторизованных HTTP-запросов к API бэкенда.

Содержит функцию, которая автоматически добавляет JWT-токен к запросам
и обрабатывает истечение срока действия access-токена (обновляя его
с помощью refresh-токена).
"""

from typing import Any

from requests import Response, Session
from requests.exceptions import RequestException
from loguru import logger

from bot.api.api_services.refresh_access_token_service import _refresh_access_token
from bot.config import bot_settings
from bot.storage import token_storage


def _authorized_request(
    session: Session,
    base_url: str,
    method: str,
    telegram_id: int,
    endpoint: str,
    **kwargs: Any,
) -> Response | None:
    """
    Выполнить HTTP-запрос к защищённому эндпоинту API.

    Добавляет заголовок Authorization: Bearer <token>. Если бэкенд
    возвращает статус 401 (Unauthorized), пытается обновить access-токен
    с помощью refresh-токена и повторить запрос.

    :param session: Сессия requests для переиспользования соединений
    :type session: Session
    :param base_url: Базовый URL API бэкенда
    :type base_url: str
    :param method: HTTP-метод (GET, POST, PATCH, DELETE)
    :type method: str
    :param telegram_id: Telegram ID пользователя для поиска токенов
    :type telegram_id: int
    :param endpoint: Путь эндпоинта (например, "/habits")
    :type endpoint: str
    :param kwargs: Дополнительные параметры для requests (json, params и т.д.)
    :raises Exception: При ошибках сети (не перехватываются здесь)
    :return: Объект ответа Response или None, если нет сохраненных токенов
    :rtype: Response | None
    """

    bundle = token_storage.get_tokens(telegram_id)

    if bundle is None:
        logger.warning("Нет сохраненных токенов для telegram_id={}", telegram_id)
        return None

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {bundle.access_token}"

    try:
        response = session.request(
            method,
            f"{base_url}{endpoint}",
            headers=headers,
            timeout=bot_settings.request_timeout,
            **kwargs,
        )

        if response.status_code == 401:
            logger.info(
                "Access-токен истёк для telegram_id={}. Пытаюсь обновить...",
                telegram_id,
            )
            if _refresh_access_token(telegram_id, session, base_url):
                bundle = token_storage.get_tokens(telegram_id)
                if bundle:
                    headers["Authorization"] = f"Bearer {bundle.access_token}"

                    response = session.request(
                        method,
                        f"{base_url}{endpoint}",
                        headers=headers,
                        timeout=bot_settings.request_timeout,
                        **kwargs,
                    )

                    if response.status_code == 401:
                        logger.warning(
                            "Запрос все еще возвращает 401 после обновления токена. "
                            "Очищаю сессию для telegram_id={}",
                            telegram_id,
                        )
                        token_storage.clear_tokens(telegram_id)
            else:
                logger.warning(
                    "Не удалось обновить токен для telegram_id={}. Требуется повторный вход.",
                    telegram_id,
                )

        return response
    except RequestException as error:
        logger.error(
            "Ошибка сети при выполнении запроса к API (telegram_id={}): {}",
            telegram_id,
            str(error),
        )
        return None
