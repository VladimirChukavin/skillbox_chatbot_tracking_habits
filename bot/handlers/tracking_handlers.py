from telebot import TeleBot
from telebot.types import Message

from bot.services.tracking_services.track_habit_service import show_track_habit
from bot.services.tracking_services.track_choice_service import show_track_choice
from bot.services.tracking_services.track_done_service import show_track_done
from bot.services.tracking_services.track_skip_service import show_track_skip


def register_tracking_handlers(bot: TeleBot) -> None:
    @bot.message_handler(commands=["track_habit"])
    def handle_track_habit(message: Message) -> None:
        show_track_habit(bot, message.from_user.id, message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("track:"))
    def handle_track_choice(call) -> None:
        show_track_choice(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("track_done:"))
    def handle_track_done(call) -> None:
        show_track_done(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("track_skip:"))
    def handle_track_skip(call) -> None:
        show_track_skip(bot, call)
