from telebot import TeleBot
from telebot.types import Message

from bot.keyboards import build_main_menu_keyboard
from bot.states import RegistrationStates
from bot.storage import token_storage


def show_start(bot: TeleBot, message: Message) -> None:
    telegram_id = message.from_user.id

    if token_storage.get_tokens(telegram_id) is not None:
        bot.send_message(
            telegram_id,
            "Вы уже авторизованы. Используйте меню ниже.",
            reply_markup=build_main_menu_keyboard(),
        )
        return

    bot.set_state(
        telegram_id, RegistrationStates.waiting_for_full_name, message.chat.id
    )
    bot.send_message(
        telegram_id,
        "Привет! Я бот для трекинга привычек. \nВведите ваше имя:",
    )
