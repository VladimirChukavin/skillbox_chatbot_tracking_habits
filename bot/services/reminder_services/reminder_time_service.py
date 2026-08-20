from loguru import logger
from telebot import TeleBot
from telebot.types import Message

from bot.api_client import api_client


def show_reminder_time(bot: TeleBot, message: Message) -> None:
    telegram_id = message.from_user.id
    raw_time = message.text.strip() if message.text else ""

    try:
        hours, minutes = (int(part) for part in raw_time.split(":"))
        if not (0 <= hours <= 23 and 0 <= minutes <= 59):
            raise ValueError
        reminder_time = f"{hours:02d}:{minutes:02d}:00"
    except ValueError:
        bot.send_message(
            telegram_id,
            "Неверный формат времени. Используйте ЧЧ:ММ, например, 09:30:",
        )
        return

    with bot.retrieve_data(telegram_id, message.chat.id) as data:
        habit_id = data.get("reminder_habit_id")

    bot.delete_state(telegram_id, message.chat.id)

    if not habit_id:
        bot.send_message(telegram_id, "Ошибка состояния. Начните заново /set_reminder")
        return

    updated = api_client.update_habit(
        telegram_id, habit_id, {"reminder_time": reminder_time}
    )

    if updated is None:
        bot.send_message(telegram_id, "❌ Не удалось установить напоминание.")
        return

    logger.bind(sent_message=True).info(
        "Установлено напоминание {} для привычки {} пользователя {}",
        reminder_time,
        habit_id,
        telegram_id,
    )
    bot.send_message(telegram_id, f"⏰ Напоминание установлено на {raw_time}!")
