"""
Потокобезопасное хранилище токенов авторизации в Redis.

Содержит класс для хранения пары токенов (access и refresh) и
класс, обеспечивающий конкурентный доступ к Redis-хранилищу.
Токены привязаны к идентификатору Telegram-пользователя и
сохраняются в Redis с ограниченным временем жизни.
"""

import json

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
    Хранилище токенов пользователей в Redis.

    Хранит токены как JSON-документы с ключами token:{telegram_id}.
    Каждая запись имеет TTL для автоматического удаления просроченных токенов.
    Redis гарантирует потокобезопасность операций, дополнительная блокировка
    не требуется.

    :ivar _client: Подключение к Redis
    :ivar _prefix: Префикс ключей в Redis (по умолчанию "token:")
    """

    def __init__(self, host: str, password: str, db: int, port: int) -> None:
        """
        Инициализировать хранилище токенов с подключением к Redis.

        Создаёт клиент с включенным декодированием ответов
        в строки (decode_responses), чтобы не парсить вручную.

        :param host: Хост Redis
        :type host: str
        :param password: Пароль Redis (может быть пустой строкой)
        :type password: str
        :param db: Номер базы данных Redis
        :type db: int
        :param port: Порт Redis
        :type port: int
        :return: Ничего не возвращает
        :rtype: None
        """

        self._client = redis.Redis(
            host=host,
            password=password,
            db=db,
            port=port,
            decode_responses=True,
        )
        self._prefix = "token:"

    def _get_key(self, telegram_id: int) -> str:
        """Сформировать ключ Redis для заданного telegram_id."""

        return f"{self._prefix}{telegram_id}"

    def save_tokens(
        self, telegram_id: int, bundle: TokenBundle, ttl_seconds: int = 2592000
    ) -> None:
        """
        Сохранить или перезаписать токены пользователя.
        Сериализует TokenBundle в JSON и сохраняет в Redis с TTL.
        При повторном вызове для того же пользователя старые токены
        перезаписываются.

        :param telegram_id: Идентификатор Telegram-пользователя
        :type telegram_id: int
        :param bundle: Контейнер с access и refresh токенами
        :type bundle: TokenBundle
        :param ttl_seconds: Срок действия токенов (30 дней)
        :type ttl_seconds: int
        :return: Ничего не возвращает
        :rtype: None
        """

        data = asdict(bundle)
        self._client.setex(self._get_key(telegram_id), ttl_seconds, json.dumps(data))

    def get_tokens(self, telegram_id: int) -> TokenBundle | None:
        """
        Получить токены пользователя.
        Читает JSON-документ из Redis и десериализует его в TokenBundle.
        Возвращает None, если ключ не существует или данные повреждены.

        :param telegram_id: Идентификатор Telegram-пользователя
        :type telegram_id: int
        :return: Контейнер с токенами или None, если токенов нет
        :rtype: TokenBundle | None
        """

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

        self._client.delete(self._get_key(telegram_id))


token_storage = TokenStorage(
    host=bot_settings.redis_host,
    password=bot_settings.redis_password,
    db=bot_settings.redis_db,
    port=bot_settings.redis_port,
)
