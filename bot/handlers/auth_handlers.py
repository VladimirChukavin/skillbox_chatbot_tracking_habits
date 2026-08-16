from telebot import TeleBot
from telebot.types import Message
from loguru import logger

from bot.api_client import api_client
from bot.keyboards import build_main_menu_keyboard
from bot.states import LoginStates, RegistrationStates
from bot.storage import token_storage


def register_auth_handlers(bot: TeleBot) -> None:
    @bot.message_handler(commands=["start"])
    def handle_start(message: Message) -> None:
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

    @bot.message_handler(state=RegistrationStates.waiting_for_full_name)
    def handle_full_name(message: Message) -> None:
        full_name = message.text.strip()

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

    @bot.message_handler(state=RegistrationStates.waiting_for_password)
    def handle_registration_password(message: Message) -> None:
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
        token_data = api_client.register_user(
            telegram_id, full_name, password, username
        )
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

    @bot.message_handler(commands=["login"])
    def handle_login_command(message: Message) -> None:
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

    @bot.message_handler(state=LoginStates.waiting_for_password)
    def handle_login_password(message: Message) -> None:
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
            bot.send_message(
                telegram_id, "❌ Неверный пароль. Попробуйте /login снова."
            )
            return

        logger.bind(sent_message=True).info(
            "Пользователь {} выполнил вход", telegram_id
        )
        bot.send_message(
            telegram_id,
            "✅ Вход выполнен, токен получен. Меню доступно.",
            reply_markup=build_main_menu_keyboard(),
        )
