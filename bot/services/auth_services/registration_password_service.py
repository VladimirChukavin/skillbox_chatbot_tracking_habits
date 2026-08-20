from loguru import logger
from telebot import TeleBot
from telebot.types import Message

from bot.api_client import api_client
from bot.keyboards import build_main_menu_keyboard


def show_registration_password(bot: TeleBot, message: Message) -> None:
    password = message.text.strip() if message.text else ""
    telegram_id = message.from_user.id

    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as error:
        logger.warning("Не удалось удалить сообщение с паролем: {}", error)

    if len(password) < 6:
        bot.send_message(
            telegram_id,
            "Пароль должен содержать не менее 6 символов. Попробуйте снова:",
        )
        return

    with bot.retrieve_data(telegram_id, message.chat.id) as data:
        full_name = data.get("full_name", message.from_user.full_name)

    username = message.from_user.username
    token_data = api_client.register_user(telegram_id, full_name, password, username)
    bot.delete_state(telegram_id, message.chat.id)

    if token_data is None:
        bot.send_message(
            telegram_id,
            "Не удалось зарегистрировать пользователя. Возможно, вы уже зарегистрированы. "
            "Используйте /login для входа.",
        )
        return

    logger.bind(sent_message=True).info(
        "Пользователь {} зарегистрирован, токен выдан", telegram_id
    )
    bot.send_message(
        telegram_id,
        "✅ Регистрация успешно завершена! Вы можете управлять привычками через меню.",
        reply_markup=build_main_menu_keyboard(),
    )
