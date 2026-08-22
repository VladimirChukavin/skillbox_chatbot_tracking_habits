from telebot import TeleBot

from bot.api.api_client import api_client
from bot.keyboards.habits_keyboard import build_habits_keyboard
from bot.states import ReminderStates


def show_set_reminder(bot: TeleBot, telegram_id: int, chat_id: int) -> None:
    habits = api_client.list_habits(telegram_id)

    if not habits:
        bot.send_message(telegram_id, "Нет привычек для установки напоминания.")
        return

    bot.set_state(telegram_id, ReminderStates.waiting_for_habit_choice, chat_id)

    bot.send_message(
        chat_id,
        "Выберите привычку:",
        reply_markup=build_habits_keyboard(habits, callback_prefix="reminder"),
    )
