from telebot import TeleBot
from telebot.types import CallbackQuery, Message


def show_cancel(bot: TeleBot, call_or_message: CallbackQuery | Message) -> None:
    if hasattr(call_or_message, "from_user"):
        telegram_id = call_or_message.from_user.id
        chat_id = call_or_message.message.chat.id
        bot.answer_callback_query(call_or_message.id)
    else:
        telegram_id = call_or_message.from_user.id
        chat_id = call_or_message.chat.id

    bot.delete_state(telegram_id, chat_id)
    bot.send_message(telegram_id, "Действие отменено.")
