from telebot import TeleBot
from telebot.types import Message
from telebot.apihelper import ApiException
from loguru import logger


def register_unknown_handlers(bot: TeleBot) -> None:
    @bot.message_handler(func=lambda message: True)
    def handle_unknown(message: Message) -> None:
        try:
            text = (
                "Извините, я вас не понимаю.\n"
                "Напишите /help, чтобы получить справку.\n"
            )

            bot.send_message(message.chat.id, text)
        except ApiException as e:
            logger.error("Ошибка при взаимодействии с API Telegram: {}".format(e))
