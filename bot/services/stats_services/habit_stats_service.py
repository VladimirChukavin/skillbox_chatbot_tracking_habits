from telebot import TeleBot

from bot.api.api_client import api_client
from bot.keyboards.habits_keyboard import build_habits_keyboard


def show_habit_stats(bot: TeleBot, telegram_id: int, chat_id: int) -> None:
    habits = api_client.list_habits(telegram_id)

    if not habits:
        bot.send_message(telegram_id, "Нет привычек для просмотра статистики.")
        return

    bot.send_message(
        telegram_id,
        "Выберите привычку:",
        reply_markup=build_habits_keyboard(habits, callback_prefix="stats"),
    )
