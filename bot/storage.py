"""
Потокобезопасное хранилище токенов авторизации.

Содержит класс для хранения пары токенов (access и refresh) и
класс, обеспечивающий конкурентный доступ к словарю токенов
через threading.Lock. Токены хранятся в памяти процесса и
привязаны к идентификатору Telegram-пользователя.
"""

import json

# import threading
from dataclasses import dataclass, asdict

import redis

from bot.config import bot_settings


@dataclass
class TokenBundle:
    """
    Контейнер для пары токенов авторизации пользователя.

    :ivar access_token: Краткосрочный токен доступа к API
    :ivar refresh_token: Долгосрочный токен для обновления access-токена
    """

    access_token: str
    refresh_token: str


class TokenStorage:
    """
    Потокобезопасное хранилище токенов пользователей в памяти.

    Хранит токены в словаре, ключами которого выступают
    идентификаторы Telegram-пользователей. Доступ к словарю
    защищён threading.Lock, что обеспечивает безопасность
    при конкурентных вызовах из разных потоков (например,
    обработчиков бота и планировщика напоминаний).

    :ivar _tokens: Словарь токенов, ключ — telegram_id, значение — TokenBundle
    :ivar _lock: Блокировка для потокобезопасного доступа
    """

    def __init__(self, host: str, port: int, db: int) -> None:
        """
        Инициализировать пустое хранилище токенов.

        Создаёт пустой словарь _tokens и блокировку
        threading.Lock для защиты конкурентного доступа.

        :return: Ничего не возвращает
        :rtype: None
        """

        # self._tokens: dict[int, TokenBundle] = {}
        # self._lock = threading.Lock()
        self._client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self._prefix = "token:"

    def _get_key(self, telegram_id: int) -> str:
        return f"{self._prefix}{telegram_id}"

    def save_tokens(
        self, telegram_id: int, bundle: TokenBundle, ttl_seconds: int = 2592000
    ) -> None:
        """
        Сохранить или перезаписать токены пользователя.

        :param telegram_id: Идентификатор Telegram-пользователя
        :type telegram_id: int
        :param bundle: Контейнер с access и refresh токенами
        :type bundle: TokenBundle
        :param ttl_seconds: Срок действия токенов
        :type ttl_seconds: int
        :return: Ничего не возвращает
        :rtype: None
        """

        # with self._lock:
        #     self._tokens[telegram_id] = bundle
        data = asdict(bundle)
        self._client.setex(self._get_key(telegram_id), ttl_seconds, json.dumps(data))

    def get_tokens(self, telegram_id: int) -> TokenBundle | None:
        """
        Получить токены пользователя.

        :param telegram_id: Идентификатор Telegram-пользователя
        :type telegram_id: int
        :return: Контейнер с токенами или None, если токенов нет
        :rtype: TokenBundle | None
        """

        # with self._lock:
        #     return self._tokens.get(telegram_id)
        data_json = self._client.get(self._get_key(telegram_id))

        if data_json is None:
            return None

        try:
            data = json.loads(data_json)
            return TokenBundle(
                access_token=data["access_token"],
                refresh_token=data["refresh_token"],
            )
        except (KeyError, json.JSONDecodeError):
            return None

    def clear_tokens(self, telegram_id: int) -> None:
        """
        Удалить токены пользователя из хранилища.

        :param telegram_id: Идентификатор Telegram-пользователя
        :type telegram_id: int
        :return: Ничего не возвращает
        :rtype: None
        """

        # with self._lock:
        #     self._tokens.pop(telegram_id, None)
        self._client.delete(self._get_key(telegram_id))


# token_storage = TokenStorage()
token_storage = TokenStorage(
    host=bot_settings.redis_host,
    port=bot_settings.redis_port,
    db=bot_settings.redis_db,
)
