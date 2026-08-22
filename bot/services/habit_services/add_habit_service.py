from telebot import TeleBot

from bot.states import AddHabitStates
from bot.storage import token_storage


def show_add_habit(bot: TeleBot, telegram_id: int, chat_id: int) -> None:
    if token_storage.get_tokens(telegram_id) is None:
        return

    bot.set_state(telegram_id, AddHabitStates.waiting_for_title, chat_id)
    bot.send_message(chat_id, "Введите название привычки:")
