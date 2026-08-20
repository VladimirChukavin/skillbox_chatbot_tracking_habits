from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.api_client import api_client
from bot.states import EditHabitStates


def show_habit_field_choice(bot: TeleBot, call: CallbackQuery) -> None:
    field = call.data.split(":")[1]
    telegram_id = call.from_user.id

    if field == "delete":
        with bot.retrieve_data(telegram_id, call.message.chat.id) as data:
            habit_id = data.get("editing_habit_id")

        if habit_id is not None and api_client.delete_habit(telegram_id, habit_id):
            bot.delete_state(telegram_id, call.message.chat.id)
            bot.edit_message_text(
                "🗑 Привычка удалена.",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        else:
            bot.send_message(telegram_id, "❌ Не удалось удалить привычку.")
        return

    with bot.retrieve_data(telegram_id, call.message.chat.id) as data:
        data["editing_field"] = field

    bot.set_state(
        telegram_id,
        EditHabitStates.waiting_for_new_value,
        call.message.chat.id,
    )
    field_labels = {
        "title": "новое название",
        "description": "новое описание",
        "target_description": "новую цель",
        "target_days": "новый срок в днях",
    }
    bot.edit_message_text(
        f"Введите {field_labels.get(field, 'новое значение')}:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )
