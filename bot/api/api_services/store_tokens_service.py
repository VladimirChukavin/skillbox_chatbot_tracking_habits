"""
Сервис для сохранения JWT-токенов в хранилище бота.

Содержит функцию для извлечения токенов из ответа API и их сохранения
в памяти бота через TokenStorage.
"""

from bot.storage import TokenBundle, token_storage


def _store_tokens(telegram_id: int, token_data: dict) -> None:
    """
    Сохранить access и refresh токены для пользователя.

    Извлекает токены из словаря token_data и сохраняет их в виде
    объекта TokenBundle в хранилище.

    :param telegram_id: Telegram ID пользователя
    :type telegram_id: int
    :param token_data: Словарь с ключами access_token и refresh_token
    :type token_data: dict
    :return: Ничего не возвращает
    :rtype: None
    """

    token_storage.save_tokens(
        telegram_id,
        TokenBundle(
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
        ),
    )
