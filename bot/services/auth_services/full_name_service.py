"""
Сервис для обработки ввода полного имени при регистрации.

Содержит функцию, которая сохраняет введённое имя в состоянии FSM
и переводит пользователя к следующему шагу (ввод пароля).
"""

from telebot import TeleBot
from telebot.types import Message

from bot.states import RegistrationStates


def show_full_name(bot: TeleBot, message: Message) -> None:
    """
    Обработать ввод полного имени пользователя при регистрации.

    Проверяет, что имя не пустое. Сохраняет имя в данных состояния (FSM)
    и переводит пользователя в состояние ожидания пароля.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param message: Входящее сообщение с именем пользователя
    :type message: Message
    :return: Ничего не возвращает
    :rtype: None
    """

    full_name = message.text.strip() if message.text else ""

    if not full_name:
        bot.send_message(
            message.from_user.id,
            "Имя не может быть пустым. Попробуйте снова:",
        )
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["full_name"] = full_name

    bot.set_state(
        message.from_user.id,
        RegistrationStates.waiting_for_password,
        message.chat.id,
    )
    bot.send_message(
        message.from_user.id,
        "Введите пароль (минимум 6 символов). "
        "⚠️ Сообщение с паролем будет удалено после ввода:",
    )
