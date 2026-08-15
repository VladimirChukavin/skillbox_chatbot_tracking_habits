import threading

import telebot.apihelper
from telebot import TeleBot
from loguru import logger

from bot.config import bot_settings
from bot.handlers.auth_handlers import register_auth_handlers
from bot.handlers.habits_handlers import register_habit_handlers
from bot.handlers.reminder_handler import register_reminder_handlers
from bot.handlers.stats_handler import register_stats_handler
from bot.handlers.tracking_handlers import register_tracking_handlers
from bot.notifier import HabitNotifier
from bot.utils.logger import configure_bot_logger


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

    try:
        bot.infinity_polling(skip_pending=True)
    except KeyboardInterrupt:
        logger.error("Остановка бота пользователем.")
    finally:
        notifier.stop()


if __name__ == "__main__":
    run_bot()
