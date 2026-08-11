from telebot import TeleBot
from telebot.types import Message
from loguru import logger

from bot.api_client import api_client
from bot.keyboards import build_habits_keyboard, build_track_keyboard
from bot.states import TrackHabitsStates


def register_tracking_handlers(bot: TeleBot) -> None:
    @bot.message_handler(commands=["track_habit"])
    def handle_track_habit(message: Message) -> None:
        telegram_id = message.from_user.id
        habits = api_client.list_habits(telegram_id)

        if not habits:
            bot.send_message(telegram_id, "Нет активных привычек для отметки.")
            return

        bot.set_state(
            telegram_id, TrackHabitsStates.waiting_for_habit_choice, message.chat.id
        )
        keyboard = build_habits_keyboard(habits, callback_prefix="track")
        bot.send_message(
            telegram_id, "Выберите привычку для отметки:", reply_markup=keyboard
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("track:"))
    def handle_track_choice(call) -> None:
        habit_id = int(call.data.split(":")[1])
        keyboard = build_track_keyboard(habit_id)
        bot.edit_message_text(
            "Отметьте выполнение:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard,
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("track_done:"))
    def handle_track_done(call) -> None:
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

    @bot.callback_query_handler(func=lambda call: call.data.startswith("track_skip:"))
    def handle_track_skip(call) -> None:
        habit_id = int(call.data.split(":")[1])
        telegram_id = call.from_user.id
        api_client.track_habit(telegram_id, habit_id, is_completed=False)
        bot.delete_state(telegram_id, call.message.chat.id)
        bot.edit_message_text(
            "❌ Отмечено как невыполненное. Привычка переносится на завтра.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )
