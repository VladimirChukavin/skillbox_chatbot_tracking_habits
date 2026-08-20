from telebot import TeleBot
from telebot.types import Message

from bot.api_client import api_client
from bot.keyboards import build_habits_keyboard
from bot.states import TrackHabitsStates


def show_track_habit(bot: TeleBot, telegram_id: int, chat_id: int) -> None:
    habits = api_client.list_habits(telegram_id)

    if not habits:
        bot.send_message(telegram_id, "Нет активных привычек для отметки.")
        return

    bot.set_state(telegram_id, TrackHabitsStates.waiting_for_habit_choice, chat_id)
    keyboard = build_habits_keyboard(habits, callback_prefix="track")
    bot.send_message(
        telegram_id, "Выберите привычку для отметки:", reply_markup=keyboard
    )
