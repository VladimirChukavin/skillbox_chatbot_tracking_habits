from loguru import logger
from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.services.habit_services.add_habit_service import show_add_habit
from bot.services.habit_services.habits_list_service import show_habits_list
from bot.services.habit_services.edit_habit_service import show_edit_habit
from bot.services.stats_services.habit_stats_service import show_habit_stats
from bot.services.tracking_services.track_habit_service import show_track_habit
from bot.services.reminder_services.set_reminder_service import show_set_reminder


def show_habit_menu_navigation(bot: TeleBot, call: CallbackQuery) -> None:
    action = call.data.split(":")[1]
    telegram_id = call.from_user.id
    chat_id = call.message.chat.id

    commands_map = {
        "add": (show_add_habit, bot, telegram_id, chat_id),
        "list": (show_habits_list, bot, telegram_id, chat_id),
        "edit": (show_edit_habit, bot, telegram_id, chat_id),
        "stats": (show_habit_stats, bot, telegram_id, chat_id),
        "track": (show_track_habit, bot, telegram_id, chat_id),
        "reminder": (show_set_reminder, bot, telegram_id, chat_id),
    }

    command_data = commands_map.get(action)

    if command_data is None:
        logger.warning("Неизвестная команда меню: {}", action)
    else:
        command_data[0](command_data[1], command_data[2], command_data[3])

    bot.answer_callback_query(call.id)
