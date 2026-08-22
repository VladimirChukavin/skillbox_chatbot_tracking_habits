from loguru import logger
from telebot import TeleBot
from telebot.types import Message

from bot.api.api_client import api_client
from bot.keyboards.main_menu_keyboard import build_main_menu_keyboard


def show_login_password(bot: TeleBot, message: Message) -> None:
    password = message.text.strip() if message.text else ""
    telegram_id = message.from_user.id

    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as error:
        logger.warning("Не удалось удалить сообщение с паролем: {}", error)

    if not password:
        bot.send_message(
            telegram_id, "Пароль не может быть пустым. Введите /login снова."
        )
        bot.delete_state(telegram_id, message.chat.id)
        return

    token_data = api_client.login_user(telegram_id, password)
    bot.delete_state(telegram_id, message.chat.id)

    if token_data is None:
        bot.send_message(telegram_id, "❌ Неверный пароль. Попробуйте /login снова.")
        return

    logger.bind(sent_message=True).info("Пользователь {} выполнил вход", telegram_id)

    bot.send_message(
        telegram_id,
        "✅ Вход выполнен, токен получен. Меню доступно.",
        reply_markup=build_main_menu_keyboard(),
    )
