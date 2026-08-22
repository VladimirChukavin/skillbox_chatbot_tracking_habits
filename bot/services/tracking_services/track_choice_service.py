from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.keyboards.track_keyboard import build_track_keyboard


def show_track_choice(bot: TeleBot, call: CallbackQuery) -> None:
    habit_id = int(call.data.split(":")[1])

    bot.edit_message_text(
        "Отметьте выполнение:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=build_track_keyboard(habit_id),
    )
