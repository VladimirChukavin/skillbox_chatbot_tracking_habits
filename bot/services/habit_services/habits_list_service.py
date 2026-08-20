from telebot import TeleBot

from bot.api_client import api_client


def show_habits_list(bot: TeleBot, telegram_id: int, chat_id: int) -> None:
    habits = api_client.list_habits(telegram_id)

    if not habits:
        bot.send_message(
            telegram_id, "У вас пока нет привычек. Добавьте через /add_habit"
        )
        return

    text_lines = ["📋 Ваши привычки:\n"]

    for index, habit in enumerate(habits, start=1):
        text_lines.append(
            f"{index}. {habit['title']} - прогресс {habit['completed_count']}/"
            f"{habit['target_days']}"
        )

    bot.send_message(telegram_id, "\n".join(text_lines), parse_mode="Markdown")
