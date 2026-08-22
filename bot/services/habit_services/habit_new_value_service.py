from loguru import logger
from telebot import TeleBot
from telebot.types import Message

from bot.api.api_client import api_client


def show_habit_new_value(bot: TeleBot, message: Message) -> None:
    telegram_id = message.from_user.id

    with bot.retrieve_data(telegram_id, message.chat.id) as data:
        habit_id = data.get("editing_habit_id")
        field = data.get("editing_field")

    if habit_id is None or field is None:
        bot.send_message(telegram_id, "Ошибка состояния. Начните заново /edit_habit")
        bot.delete_state(telegram_id, message.chat.id)
        return

    if not message.text:
        bot.send_message(telegram_id, "Пожалуйста, введите текстовое значение:")
        return

    value: str | int = message.text.strip()

    if not value:
        bot.send_message(telegram_id, "Значение не может быть пустым:")
        return

    if field == "target_days":
        try:
            value = int(value)
        except ValueError:
            bot.send_message(telegram_id, "Введите число:")
            return

    update_payload = {field: value}
    updated = api_client.update_habit(telegram_id, habit_id, update_payload)
    bot.delete_state(telegram_id, message.chat.id)

    if updated is None:
        bot.send_message(telegram_id, "❌ Не удалось обновить привычку.")
        return

    logger.bind(sent_message=True).info(
        "Привычка {} обновлена пользователем {}", habit_id, telegram_id
    )
    bot.send_message(telegram_id, "✅ Привычка обновлена!")
