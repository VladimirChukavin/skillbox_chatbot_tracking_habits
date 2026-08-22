from loguru import logger
from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.api.api_client import api_client


def show_track_done(bot: TeleBot, call: CallbackQuery) -> None:
    habit_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id
    result = api_client.track_habit(telegram_id, habit_id, is_completed=True)
    bot.delete_state(telegram_id, call.message.chat.id)

    if result is None:
        bot.answer_callback_query(call.id, "Ошибка при отметке")
        return

    progress = f"{result['completed_count']}/{result['target_days']}"
    bot.edit_message_text(
        f"✅ Отмечено как выполненное! Прогресс: {progress}",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )
    logger.bind(sent_message=True).info(
        "Привычка {} отмечена выполненной пользователем {}", habit_id, telegram_id
    )
