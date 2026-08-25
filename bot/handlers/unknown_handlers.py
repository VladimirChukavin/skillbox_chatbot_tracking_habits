"""
Обработчик неизвестных команд и сообщений.

Содержит функцию регистрации catch-all хендлера, который перехватывает
все текстовые сообщения, не соответствующие ни одной другой команде,
и предлагает пользователю воспользоваться справкой.
"""

from telebot import TeleBot
from telebot.types import Message
from telebot.apihelper import ApiException
from loguru import logger


def register_unknown_handlers(bot: TeleBot) -> None:
    """
    Зарегистрировать обработчик для всех нераспознанных сообщений.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :return: Ничего не возвращает
    :rtype: None
    """

    @bot.message_handler(func=lambda message: True)
    def handle_unknown(message: Message) -> None:
        """
        Отправить сообщение о нераспознанной команде.

        Предлагает пользователю ввести /help для получения списка доступных команд.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :raises ApiException: При ошибке отправки сообщения в Telegram
        :return: Ничего не возвращает
        :rtype: None
        """

        try:
            text = (
                "Извините, я вас не понимаю.\n"
                "Напишите /help, чтобы получить справку.\n"
            )

            bot.send_message(message.chat.id, text)
        except ApiException as e:
            logger.error("Ошибка при взаимодействии с API Telegram: {}".format(e))
