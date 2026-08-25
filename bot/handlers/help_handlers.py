"""
Обработчик команды /help и текстового сообщения "Справка".

Содержит функцию регистрации хендлера, который формирует и отправляет
пользователю список доступных команд бота.
"""

from telebot import TeleBot
from telebot.types import Message
from telebot.apihelper import ApiException
from loguru import logger

from bot.config import DEFAULT_COMMANDS


def register_help_handler(bot: TeleBot) -> None:
    """
    Зарегистрировать обработчик для команды /help и слова "Справка".

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :return: Ничего не возвращает
    :rtype: None
    """

    @bot.message_handler(commands=["help"])
    @bot.message_handler(func=lambda message: message.text == "Справка")
    def handle_help(message: Message) -> None:
        """
        Отправить пользователю список доступных команд.

        Формирует текст справки на основе DEFAULT_COMMANDS из конфигурации.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :raises ApiException: При ошибке отправки сообщения в Telegram
        :return: Ничего не возвращает
        :rtype: None
        """

        try:
            commands = [f"/{command} - {desc}" for command, desc in DEFAULT_COMMANDS]
            text = (
                "Я не волшебник, я только бот, который предоставляет вам возможности отслеживания привычек.\n"
                "Ниже список команд, которыми вы может воспользоваться.\n{}"
            ).format("\n".join(commands))

            bot.send_message(message.chat.id, text)
        except ApiException as e:
            logger.error("Ошибка при взаимодействии с API Telegram: {}".format(e))
