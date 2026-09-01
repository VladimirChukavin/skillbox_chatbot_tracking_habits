"""
Сервис для обработки ввода пароля при входе пользователя.

Содержит функцию, которая проверяет пароль через API бэкенда,
сохраняет токены и показывает главное меню при успешной аутентификации.
"""

from loguru import logger
from telebot import TeleBot
from telebot.types import Message
from telebot.apihelper import ApiException

from bot.api.api_client import api_client
from bot.keyboards.main_menu_keyboard import build_main_menu_keyboard


def show_login_password(bot: TeleBot, message: Message) -> None:
    """
    Обработать ввод пароля для входа в систему.

    Удаляет сообщение с паролем из чата в целях безопасности. Отправляет
    запрос на аутентификацию к бэкенду. При успехе сбрасывает состояние (FSM)
    и отправляет пользователю главное меню. При неудаче просит попробовать снова.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param message: Входящее сообщение с паролем
    :type message: Message
    :return: Ничего не возвращает
    :rtype: None
    """

    password = message.text.strip() if message.text else ""
    telegram_id = message.from_user.id
    chat_id = message.chat.id

    try:
        bot.delete_message(chat_id, message.message_id)
    except ApiException as error:
        logger.warning("Не удалось удалить сообщение с паролем: {}", error)

    if not password:
        bot.send_message(
            telegram_id, "Пароль не может быть пустым. Введите /login снова."
        )
        bot.delete_state(telegram_id, chat_id)
        return

    token_data = api_client.login_user(telegram_id, password)
    bot.delete_state(telegram_id, chat_id)

    if token_data is None:
        bot.send_message(telegram_id, "❌ Неверный пароль. Попробуйте /login снова.")
        return

    logger.bind(sent_message=True).info("Пользователь {} выполнил вход", telegram_id)

    bot.send_message(
        telegram_id,
        "✅ Вход выполнен, токен получен. Меню доступно.",
        reply_markup=build_main_menu_keyboard(),
    )
