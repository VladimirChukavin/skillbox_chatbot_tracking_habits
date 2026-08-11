from telebot import TeleBot
from telebot.types import Message

from bot.api_client import api_client
from bot.keyboards import build_habits_keyboard


def register_stats_handler(bot: TeleBot) -> None:
    @bot.message_handler(commands=["habit_stats"])
    def handle_habit_stats(message: Message) -> None:
        telegram_id = message.from_user.id
        habits = api_client.list_habits(telegram_id)

        if not habits:
            bot.send_message(telegram_id, "Нет привычек для просмотра статистики.")
            return

        keyboard = build_habits_keyboard(habits, callback_prefix="stats")
        bot.send_message(telegram_id, "Выберите привычку:", reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("stats:"))
    def handle_stats_choice(call) -> None:
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
            f"*Статистика по привычке \"{stats['title']}\"*\n\n"
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
