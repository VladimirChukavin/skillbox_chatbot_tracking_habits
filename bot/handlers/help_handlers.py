from telebot import TeleBot
from telebot.types import Message
from telebot.apihelper import ApiException
from loguru import logger

from bot.config import DEFAULT_COMMANDS


def register_help_handler(bot: TeleBot) -> None:
    @bot.message_handler(commands=["help"])
    @bot.message_handler(func=lambda message: message.text == "Справка")
    def handle_help(message: Message) -> None:
        try:
            commands = [f"/{command} - {desc}" for command, desc in DEFAULT_COMMANDS]
            text = (
                "Я не волшебник, я только бот, который предоставляет вам возможности отслеживания привычек.\n"
                "Ниже список команд, которыми вы может воспользоваться.\n{}"
            ).format("\n".join(commands))

            bot.send_message(message.chat.id, text)
        except ApiException as e:
            logger.error("Ошибка при взаимодействии с API Telegram: {}".format(e))
