from telebot import TeleBot
from telebot.types import Message

from bot.states import AddHabitStates


def show_habit_description(bot: TeleBot, message: Message) -> None:
    description = message.text.strip() if message.text else ""

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["description"] = None if description == "-" else description

    bot.set_state(
        message.from_user.id,
        AddHabitStates.waiting_for_target_description,
        message.chat.id,
    )
    bot.send_message(
        message.from_user.id, "Введите цель привычки (или '-' чтобы пропустить):"
    )
