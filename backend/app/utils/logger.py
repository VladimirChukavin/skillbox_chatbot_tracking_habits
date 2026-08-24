"""
Утилита для настройки логирования бэкенда.

Содержит функцию для конфигурации логгера Loguru с выводом в консоль
и записью в файлы с ротацией и сжатием.
"""

import sys

from loguru import logger


def configure_logger(debug: bool = False) -> None:
    """
    Настроить логгер приложения (Loguru).

    Удаляет стандартные обработчики и добавляет новые:
    - Вывод в консоль (stdout) с цветным форматированием.
    - Запись в файл logs/backend_{time}.log с ротацией каждые 10 MB,
      хранением 14 дней и сжатием в zip.

    :param debug: Флаг включения режима отладки. Если True, уровень логирования
        устанавливается в DEBUG, иначе в INFO. По умолчанию False.
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
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
    )
    logger.add(
        "logs/backend_{time}.log",
        level=log_level,
        rotation="10 MB",
        retention="14 days",
        compression="zip",
        encoding="utf-8",
    )
