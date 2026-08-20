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
    @bot.message_handler(commands=["start"])
    def handle_start(message: Message) -> None:
        show_start(bot, message)

    @bot.message_handler(state=RegistrationStates.waiting_for_full_name)
    def handle_full_name(message: Message) -> None:
        show_full_name(bot, message)

    @bot.message_handler(state=RegistrationStates.waiting_for_password)
    def handle_registration_password(message: Message) -> None:
        show_registration_password(bot, message)

    @bot.message_handler(commands=["login"])
    def handle_login_command(message: Message) -> None:
        show_login_command(bot, message)

    @bot.message_handler(state=LoginStates.waiting_for_password)
    def handle_login_password(message: Message) -> None:
        show_login_password(bot, message)
