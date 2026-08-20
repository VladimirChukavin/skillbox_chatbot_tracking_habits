from telebot import TeleBot
from telebot.types import Message

from bot.services.stats_services.habit_stats_service import show_habit_stats
from bot.services.stats_services.stats_choice_service import show_stats_choice


def register_stats_handler(bot: TeleBot) -> None:
    @bot.message_handler(commands=["habit_stats"])
    def handle_habit_stats(message: Message) -> None:
        show_habit_stats(bot, message.from_user.id, message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("stats:"))
    def handle_stats_choice(call) -> None:
        show_stats_choice(bot, call)
