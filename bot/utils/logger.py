"""
Конфигурация логгера бота на базе loguru.

Содержит функцию для настройки вывода логов в консоль и файлы:
основной лог с ротацией по размеру и времени хранения, а также
отдельный лог отправленных сообщений, фильтруемый по extra-данным.
"""

import sys

from loguru import logger


def configure_bot_logger(debug: bool = False) -> None:
    """
    Настроить логгер бота.

    Удаляет все существующие обработчики логгера loguru и
    добавляет три новых:
    1. Консольный вывод (sys.stdout) — с цветным форматированием,
       включающим время, уровень, имя модуля и сообщение. Уровень
       логирования зависит от параметра debug: "DEBUG" при
       True, иначе "INFO".
    2. Основной файл (logs/bot_{time}.log) — с ротацией при
       достижении 10 МБ, хранением 14 дней и сжатием в zip.
    3. Файл отправленных сообщений (logs/bot_sent_messages.log) —
       записи с уровнем "INFO", ротацией 10 МБ, хранением 30 дней,
       сжатием в zip. Фильтруется по наличию ключа
       "sent_messages" в record["extra"], что позволяет
       выделять логи отправленных пользователю сообщений.

    :param debug: Флаг включения отладочного уровня логирования.
        Если True — устанавливается уровень "DEBUG",
        иначе "INFO".
    :type debug: bool
    :return: Ничего не возвращает
    :rtype: None
    """

    logger.remove()
    log_level = "DEBUG" if debug else "INFO"
    logger.add(
        sys.stdout,
        level=log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | <cyan>{name}</cyan> | <level>{message}</level>"
        ),
    )
    logger.add(
        "logs/bot_{time}.log",
        level=log_level,
        rotation="10 MB",
        retention="14 days",
        compression="zip",
        encoding="utf-8",
    )
    logger.add(
        "logs/bot_sent_messages.log",
        level="INFO",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
        filter=lambda record: "sent_messages" in record["extra"],
    )
