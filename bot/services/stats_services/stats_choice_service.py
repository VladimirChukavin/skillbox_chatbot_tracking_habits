from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.api_client import api_client


def show_stats_choice(bot: TeleBot, call: CallbackQuery) -> None:
    habit_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id
    stats = api_client.get_habit_stats(telegram_id, habit_id)

    if stats is None:
        bot.answer_callback_query(call.id, "Не удалось получить статистику.")
        return

    today_mark = (
        "✅ выполнена сегодня"
        if stats["is_completed_today"]
        else "⬜ не отмечена сегодня"
    )
    text = (
        f"Статистика по привычке \"{stats['title']}\"\n\n"
        f"Выполнено: {stats['completed_count']} из {stats['target_days']} дней\n"
        f"Прогресс: {stats['progress_percent']}%\n"
        f"Сегодня: {today_mark}"
    )
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="Markdown",
    )
