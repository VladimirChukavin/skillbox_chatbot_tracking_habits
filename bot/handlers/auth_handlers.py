"""
Обработчики сообщений и состояний для аутентификации пользователей.

Содержит функцию регистрации хендлеров для команд /start и /login,
а также для пошаговых состояний регистрации и входа (FSM).
"""

from telebot import TeleBot
from telebot.types import Message

from bot.services.auth_services.start_service import show_start
from bot.services.auth_services.full_name_service import show_full_name
from bot.services.auth_services.registration_password_service import (
    show_registration_password,
)
from bot.services.auth_services.login_command_service import show_login_command
from bot.services.auth_services.login_password_service import show_login_password
from bot.states import LoginStates, RegistrationStates


def register_auth_handlers(bot: TeleBot) -> None:
    """
    Зарегистрировать обработчики для аутентификации и регистрации.

    Связывает команды и состояния пользователя (FSM) с соответствующими
    сервисными функциями.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :return: Ничего не возвращает
    :rtype: None
    """

    @bot.message_handler(commands=["start"])
    def handle_start(message: Message) -> None:
        """
        Обработчик команды /start.

        Вызывает сервисную функцию для приветствия и проверки авторизации.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_start(bot, message)

    @bot.message_handler(state=RegistrationStates.waiting_for_full_name)
    def handle_full_name(message: Message) -> None:
        """
        Обработчик состояния ожидания полного имени (при регистрации).

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_full_name(bot, message)

    @bot.message_handler(state=RegistrationStates.waiting_for_password)
    def handle_registration_password(message: Message) -> None:
        """
        Обработчик состояния ожидания пароля (при регистрации).

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_registration_password(bot, message)

    @bot.message_handler(commands=["login"])
    def handle_login_command(message: Message) -> None:
        """
        Обработчик команды /login.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_login_command(bot, message)

    @bot.message_handler(state=LoginStates.waiting_for_password)
    def handle_login_password(message: Message) -> None:
        """
        Обработчик состояния ожидания пароля (при входе).

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_login_password(bot, message)
