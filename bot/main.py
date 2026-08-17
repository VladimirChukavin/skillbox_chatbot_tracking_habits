import time

import telebot.apihelper
from telebot import TeleBot
from loguru import logger
from telebot.types import BotCommand
from requests.exceptions import ConnectionError

from bot.config import bot_settings
from bot.handlers.auth_handlers import register_auth_handlers
from bot.handlers.habits_handlers import register_habit_handlers
from bot.handlers.reminder_handler import register_reminder_handlers
from bot.handlers.stats_handler import register_stats_handler
from bot.handlers.tracking_handlers import register_tracking_handlers
from bot.notifier import HabitNotifier
from bot.utils.logger import configure_bot_logger

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("login", "Введите пароль для получения токена на новую сессию"),
    ("add_habit", "Введите название привычки"),
    ("habits", "Ваши привычки"),
    ("edit_habit", "Редактировать привычку"),
    ("set_reminder", "Установить напоминание"),
    ("habit_stats", "Статистика привычек"),
    ("track_habit", "Выберите привычку для трекинга"),
)


def create_bot() -> TeleBot:
    proxy = None

    if bot_settings.http_proxy:
        proxy = bot_settings.http_proxy

    bot = TeleBot(bot_settings.telegram_token, use_class_middlewares=True)

    if proxy:
        telebot.apihelper.proxy = {"http": proxy, "https": proxy}

    register_auth_handlers(bot)
    register_habit_handlers(bot)
    register_reminder_handlers(bot)
    register_stats_handler(bot)
    register_tracking_handlers(bot)
    return bot


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
