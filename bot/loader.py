"""
Фабрика создания и настройки экземпляра Telegram-бота.

Содержит функцию, которая инициализирует бота на основе
настроек из bot_settings, регистрирует кастомные фильтры,
прокси и все обработчики команд и callback-запросов проекта.
"""

import telebot.apihelper
from telebot import TeleBot, custom_filters

from bot.config import bot_settings
from bot.handlers.auth_handlers import register_auth_handlers
from bot.handlers.habits_handlers import register_habit_handlers
from bot.handlers.help_handlers import register_help_handler
from bot.handlers.reminder_handler import register_reminder_handlers
from bot.handlers.stats_handler import register_stats_handler
from bot.handlers.tracking_handlers import register_tracking_handlers
from bot.handlers.unknown_handlers import register_unknown_handlers


def create_bot() -> TeleBot:
    """
    Создать и настроить экземпляр Telegram-бота.

    Читает URL HTTP-прокси из bot_settings.http_proxy (если задан)
    и применяет его к telebot.apihelper.proxy для HTTP и HTTPS.
    Инициализирует TeleBot с токеном из настроек и поддержкой
    классовых middleware (use_class_middlewares=True).

    Регистрирует кастомный фильтр StateFilter для работы с
    FSM-состояниями и подключает все группы обработчиков:
    - register_auth_handlers — авторизация и регистрация;
    - register_habit_handlers — создание, редактирование,
      удаление привычек;
    - register_reminder_handlers — установка напоминаний;
    - register_stats_handler — просмотр статистики;
    - register_tracking_handlers — отметка выполнения;
    - register_help_handler — справка по командам;
    - register_unknown_handlers — обработка неизвестных команд.

    :return: Настроенный экземпляр Telegram-бота, готовый к запуску
    :rtype: TeleBot
    """

    proxy = None

    if bot_settings.http_proxy:
        proxy = bot_settings.http_proxy

    bot = TeleBot(bot_settings.telegram_token, use_class_middlewares=True)
    bot.add_custom_filter(custom_filters.StateFilter(bot))

    if proxy:
        telebot.apihelper.proxy = {"http": proxy, "https": proxy}

    register_auth_handlers(bot)
    register_habit_handlers(bot)
    register_reminder_handlers(bot)
    register_stats_handler(bot)
    register_tracking_handlers(bot)
    register_help_handler(bot)
    register_unknown_handlers(bot)

    return bot
