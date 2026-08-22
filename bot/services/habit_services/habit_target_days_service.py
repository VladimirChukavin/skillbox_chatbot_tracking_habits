from loguru import logger
from telebot import TeleBot
from telebot.types import Message

from bot.api.api_client import api_client


def show_habit_target_days(bot: TeleBot, message: Message) -> None:
    telegram_id = message.from_user.id

    if not isinstance(message.text, str):
        bot.send_message(telegram_id, "Пожалуйста, введите число от 1 до 365:")
        return

    raw_days = message.text.strip()

    try:
        target_days = int(raw_days)
        if target_days < 1 or target_days > 365:
            raise ValueError
    except ValueError:
        bot.send_message(telegram_id, "Введите число от 1 до 365:")
        return

    with bot.retrieve_data(telegram_id, message.chat.id) as data:
        habit_data = {
            "title": data.get("title"),
            "description": data.get("description"),
            "target_description": data.get("target_description"),
            "target_days": target_days,
        }

    bot.delete_state(telegram_id, message.chat.id)

    created = api_client.create_habit(telegram_id, habit_data)

    if created is None:
        bot.send_message(
            telegram_id, "❌ Не удалось создать привычку. Вы авторизованы? /login"
        )
        return

    logger.bind(sent_message=True).info(
        "Создана привычка {} для пользователя {}", created.get("title"), telegram_id
    )
    bot.send_message(telegram_id, f"✅ Привычка \"{created['title']}\" добавлена!")
