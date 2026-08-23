from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.api.api_client import api_client


def show_delete_habit_choice(bot: TeleBot, call: CallbackQuery) -> None:
    habit_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id

    if api_client.delete_habit(telegram_id, habit_id):
        bot.delete_state(telegram_id, call.message.chat.id)
        bot.edit_message_text(
            "🗑 Привычка удалена.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )
    else:
        bot.send_message(telegram_id, "❌ Не удалось удалить привычку.")
