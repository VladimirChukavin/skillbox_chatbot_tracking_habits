"""
Сервис для обработки команды /login.

Содержит функцию, которая переводит пользователя в состояние ожидания
пароля (FSM) для последующей аутентификации на бэкенде.
"""

from telebot import TeleBot
from telebot.types import Message

from bot.states import LoginStates


def show_login_command(bot: TeleBot, message: Message) -> None:
    """
    Инициировать процесс входа пользователя в систему.

    Устанавливает состояние (FSM) ожидания ввода пароля и отправляет
    пользователю соответствующее сообщение.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param message: Входящее сообщение (команда /login)
    :type message: Message
    :return: Ничего не возвращает
    :rtype: None
    """

    telegram_id = message.from_user.id
    bot.set_state(
        telegram_id,
        LoginStates.waiting_for_password,
        message.chat.id,
    )
    bot.send_message(
        telegram_id,
        "Введите пароль для получения токена на новую сессию.\n"
        'Для отмены введите "cancel".\n'
        "⚠️ Сообщение будет удалено.",
    )
