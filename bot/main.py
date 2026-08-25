"""
Точка входа в Telegram-бота для трекинга привычек.

Содержит функцию, которая настраивает логгер, создаёт
экземпляр бота, запускает фоновый планировщик напоминаний,
регистрирует команды бота и поддерживает долгий polling-цикл
с автоматическим переподключением при сбоях сети.
"""

import time

from loguru import logger
from telebot.types import BotCommand
from requests.exceptions import ConnectionError

from bot.config import bot_settings, DEFAULT_COMMANDS
from bot.loader import create_bot
from bot.notifier import HabitNotifier
from bot.utils.logger import configure_bot_logger


def run_bot() -> None:
    """
    Запустить Telegram-бота и планировщик напоминаний.

    Настраивает логгер через configure_bot_logger с уровнем
    логирования, зависящим от bot_settings.debug. Создаёт
    экземпляр бота функцией create_bot, инициализирует
    HabitNotifier с фоновым планировщиком APScheduler и
    запускает его методом start.

    Регистрирует команды бота из DEFAULT_COMMANDS через
    bot.set_my_commands для отображения в меню Telegram.

    Запускает долгий polling-цикл bot.infinity_polling с
    параметром long_polling_timeout=30. На первой итерации
    (first_run = True) сбрасывает накопленные обновления
    (skip_pending=True), на последующих — False.

    Обрабатывает исключения:
    - ConnectionError — записывает предупреждение в лог,
      ждёт 5 секунд и переподключается;
    - KeyboardInterrupt — записывает сообщение об остановке
      пользователем и выходит из цикла;
    - Exception — записывает непредвиденную ошибку в лог,
      ждёт 5 секунд и переподключается.

    После выхода из цикла останавливает планировщик напоминаний
    методом notifier.stop.

    :return: Ничего не возвращает
    :rtype: None
    """

    configure_bot_logger(debug=bot_settings.debug)
    bot = create_bot()
    notifier = HabitNotifier(bot)
    notifier.start()

    logger.info("Запуск Telegram-бота для трекинга привычек.")

    bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS])

    first_run = True
    while True:
        try:
            bot.infinity_polling(skip_pending=first_run, long_polling_timeout=30)
            first_run = False
        except ConnectionError as error:
            logger.warning("Соединение разорвано, переподключение: {}", error)
            time.sleep(5)
            first_run = False
        except KeyboardInterrupt:
            logger.error("Остановка бота пользователем.")
            break
        except Exception as error:
            logger.error("Непредвиденная ошибка polling: {}", error)
            time.sleep(5)
            first_run = False

    notifier.stop()


if __name__ == "__main__":
    run_bot()
