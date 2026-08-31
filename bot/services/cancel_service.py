from telebot import TeleBot
from telebot.types import CallbackQuery


def show_cancel(bot: TeleBot, call: CallbackQuery) -> None:
    telegram_id = call.from_user.id
    chat_id = call.message.chat.id

    bot.delete_state(telegram_id, chat_id)
    bot.send_message(telegram_id, "Действие отменено.")
    bot.answer_callback_query(call.id)
