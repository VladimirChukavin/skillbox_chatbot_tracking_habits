import time

from loguru import logger
from telebot.types import BotCommand
from requests.exceptions import ConnectionError

from bot.config import bot_settings, DEFAULT_COMMANDS
from bot.loader import create_bot
from bot.notifier import HabitNotifier
from bot.utils.logger import configure_bot_logger


def run_bot() -> None:
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
