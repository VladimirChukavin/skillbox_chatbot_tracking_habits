"""
Сервис обработки команды /start.

Содержит функцию, которая проверяет авторизацию пользователя
и либо показывает главное меню (если токены уже есть),
либо инициирует процесс регистрации.
"""

from telebot import TeleBot
from telebot.types import Message

from bot.keyboards.main_menu_keyboard import build_main_menu_keyboard
from bot.states import RegistrationStates
from bot.storage import token_storage


def show_start(bot: TeleBot, message: Message) -> None:
    """
    Обработать команду /start.

    Проверяет наличие сохранённых токенов авторизации для текущего
    Telegram-пользователя. Если токены найдены — отправляет сообщение
    об успешной авторизации и показывает главное меню. Если токенов
    нет — переводит пользователя в состояние ожидания ввода полного
    имени (первый шаг регистрации) и отправляет приветственное сообщение.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param message: Входящее сообщение от команды /start
    :type message: Message
    :return: Ничего не возвращает
    :rtype: None
    """

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
