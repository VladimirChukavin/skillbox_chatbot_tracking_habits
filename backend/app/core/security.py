"""
Утилиты безопасности для аутентификации и работы с JWT-токенами.

Содержит функции для хеширования паролей, а также создания
и декодирования JSON Web Tokens (access и refresh токенов).
"""

import datetime
from typing import Any

import bcrypt
from jose import jwt

from app.config import get_settings

settings = get_settings()


def hash_password(raw_password: str) -> str:
    """
    Хешировать пароль с использованием алгоритма bcrypt.

    Генерирует случайную соль и создаёт хеш пароля, безопасный для
    хранения в базе данных.

    :param raw_password: Пароль в открытом виде
    :type raw_password: str
    :return: Хешированный пароль
    :rtype: str
    """

    return bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(raw_password: str, hashed_password: str) -> bool:
    """
    Проверить соответствие пароля его хешу.

    :param raw_password: Пароль в открытом виде для проверки
    :type raw_password: str
    :param hashed_password: Хеш пароля, сохранённый в базе данных
    :type hashed_password: str
    :return: True, если пароль соответствует хешу, иначе False
    :rtype: bool
    """

    return bcrypt.checkpw(raw_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_token(telegram_id: int, user_id: int, token_type: str = "access") -> str:
    """
    Создать JWT-токен (access или refresh).

    Формирует полезную нагрузку (payload) с идентификатором пользователя,
    типом токена и сроком действия, затем кодирует её с использованием
    секретного ключа и алгоритма из настроек приложения.

    :param telegram_id: Telegram ID пользователя
    :type telegram_id: int
    :param user_id: Внутренний ID пользователя в БД
    :type user_id: int
    :param token_type: Тип токена ("access" или "refresh"), defaults to "access"
    :type token_type: str, optional
    :return: Закодированная строка JWT-токена
    :rtype: str
    """

    now = datetime.datetime.now(datetime.timezone.utc)

    if token_type == "access":
        expire = now + datetime.timedelta(minutes=settings.access_token_expire_minutes)
    else:
        expire = now + datetime.timedelta(days=settings.refresh_token_expire_days)

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "telegram_id": telegram_id,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict[str, Any]:
    """
    Декодировать JWT-токен и проверить его валидность.

    :param token: Закодированная строка JWT-токена
    :type token: str
    :raises JWTError: Если токен недействителен, подпись не совпадает
        или срок действия истёк
    :return: Словарь с полезной нагрузкой (payload) токена
    :rtype: dict[str, Any]
    """

    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
