"""
Потокобезопасное хранилище токенов авторизации.

Содержит класс для хранения пары токенов (access и refresh) и
класс, обеспечивающий конкурентный доступ к словарю токенов
через threading.Lock. Токены хранятся в памяти процесса и
привязаны к идентификатору Telegram-пользователя.
"""

import threading
from dataclasses import dataclass


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

    def __init__(self) -> None:
        """
        Инициализировать пустое хранилище токенов.

        Создаёт пустой словарь _tokens и блокировку
        threading.Lock для защиты конкурентного доступа.

        :return: Ничего не возвращает
        :rtype: None
        """

        self._tokens: dict[int, TokenBundle] = {}
        self._lock = threading.Lock()

    def save_tokens(self, telegram_id: int, bundle: TokenBundle) -> None:
        """
        Сохранить или перезаписать токены пользователя.

        :param telegram_id: Идентификатор Telegram-пользователя
        :type telegram_id: int
        :param bundle: Контейнер с access и refresh токенами
        :type bundle: TokenBundle
        :return: Ничего не возвращает
        :rtype: None
        """

        with self._lock:
            self._tokens[telegram_id] = bundle

    def get_tokens(self, telegram_id: int) -> TokenBundle | None:
        """
        Получить токены пользователя.

        :param telegram_id: Идентификатор Telegram-пользователя
        :type telegram_id: int
        :return: Контейнер с токенами или None, если токенов нет
        :rtype: TokenBundle | None
        """

        with self._lock:
            return self._tokens.get(telegram_id)

    def clear_tokens(self, telegram_id: int) -> None:
        """
        Удалить токены пользователя из хранилища.

        :param telegram_id: Идентификатор Telegram-пользователя
        :type telegram_id: int
        :return: Ничего не возвращает
        :rtype: None
        """

        with self._lock:
            self._tokens.pop(telegram_id, None)


token_storage = TokenStorage()
