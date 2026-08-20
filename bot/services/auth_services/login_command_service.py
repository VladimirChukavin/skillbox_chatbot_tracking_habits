from telebot import TeleBot
from telebot.types import Message

from bot.states import LoginStates


def show_login_command(bot: TeleBot, message: Message) -> None:
    telegram_id = message.from_user.id
    bot.set_state(
        telegram_id,
        LoginStates.waiting_for_password,
        message.chat.id,
    )
    bot.send_message(
        telegram_id,
        "Введите пароль для получения токена на новую сессию.\n"
        "⚠️ Сообщение будет удалено.",
    )
