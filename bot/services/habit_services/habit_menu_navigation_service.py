"""
Сервис навигации по главному меню привычек.

Содержит функцию-диспетчер, которая вызывается при нажатии
inline-кнопки главного меню. Функция определяет выбранное действие
по callback-данным и делегирует выполнение соответствующему
сервису (добавление, список, редактирование, статистика, отметка,
напоминание, удаление).
"""

from loguru import logger
from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.services.habit_services.add_habit_service import show_add_habit
from bot.services.habit_services.delete_habit_service import show_delete_habit
from bot.services.habit_services.habits_list_service import show_habits_list
from bot.services.habit_services.edit_habit_service import show_edit_habit
from bot.services.stats_services.habit_stats_service import show_habit_stats
from bot.services.tracking_services.track_habit_service import show_track_habit
from bot.services.reminder_services.set_reminder_service import show_set_reminder


def show_habit_menu_navigation(bot: TeleBot, call: CallbackQuery) -> None:
    """
    Обработать нажатие кнопки главного меню привычек.

    Извлекает действие из callback-данных формата "menu:<action>"
    и ищет соответствующий обработчик в словаре commands_map,
    который связывает ключ действия с кортежем из функции-обработчика
    и её аргументов (bot, telegram_id, chat_id).

    Если действие найдено — вызывает соответствующий сервис с нужными
    аргументами. Если действие неизвестно — записывает предупреждение
    в лог через loguru.logger. В конце подтверждает обработку
    callback-запроса методом answer_callback_query, чтобы убрать
    индикатор загрузки на кнопке.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param call: Callback-запрос от inline-кнопки главного меню
    :type call: CallbackQuery
    :return: Ничего не возвращает
    :rtype: None
    """

    telegram_id = call.from_user.id
    chat_id = call.message.chat.id

    parts = call.data.split(":")

    if len(parts) != 2 or parts[0] != "menu":
        logger.warning("Некорректный формат callback-данных: {}", call.data)
        bot.answer_callback_query(call.id, "Ошибка: некорректная команда.")
        return

    action = parts[1]

    commands_map = {
        "add": show_add_habit,
        "list": show_habits_list,
        "edit": show_edit_habit,
        "stats": show_habit_stats,
        "track": show_track_habit,
        "reminder": show_set_reminder,
        "delete": show_delete_habit,
    }

    handler = commands_map.get(action)

    if handler is None:
        logger.warning("Неизвестная команда меню: {}", action)
        bot.answer_callback_query(call.id, "Ошибка: неизвестная команда.")
        bot.send_message(chat_id, "Неизвестная команда. Выберите команду из меню.")
    else:
        handler(bot, telegram_id, chat_id)
        bot.answer_callback_query(call.id)
