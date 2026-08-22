from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.api.api_client import api_client


def show_track_skip(bot: TeleBot, call: CallbackQuery) -> None:
    habit_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id
    result = api_client.track_habit(telegram_id, habit_id, is_completed=False)
    bot.delete_state(telegram_id, call.message.chat.id)

    if result is None:
        bot.edit_message_text(
            "❌ Ошибка при отметке.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )
        return

    bot.edit_message_text(
        "❌ Отмечено как невыполненное. Привычка переносится на завтра.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )
