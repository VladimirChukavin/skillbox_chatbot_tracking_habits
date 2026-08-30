"""
Сервис для сохранения JWT-токенов в хранилище бота.

Содержит функцию для извлечения токенов из ответа API и их сохранения
в памяти бота через TokenStorage.
"""

from loguru import logger

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

    try:
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")

        if not access_token or not refresh_token:
            logger.error(
                "Неполный ответ с токенами (telegram_id={}): {}",
                telegram_id,
                token_data,
            )
            return

        token_storage.save_tokens(
            telegram_id,
            TokenBundle(
                access_token=access_token,
                refresh_token=refresh_token,
            ),
        )

        logger.debug(
            "Токены успешно сохранены (telegram_id={})",
            telegram_id,
        )
    except Exception as error:
        logger.error(
            "Критическая ошибка при сохранении токенов (telegram_id={}): {}",
            telegram_id,
            str(error),
        )
