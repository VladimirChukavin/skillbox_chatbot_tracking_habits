from telebot import TeleBot
from telebot.types import Message

from bot.states import AddHabitStates


def show_habit_target(bot: TeleBot, message: Message) -> None:
    target_description = message.text.strip() if message.text else ""

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["target_description"] = (
            None if target_description == "-" else target_description
        )

    bot.set_state(
        message.from_user.id,
        AddHabitStates.waiting_for_target_days,
        message.chat.id,
    )
    bot.send_message(
        message.from_user.id, "Введите срок выполнения в днях (по умолчанию 21):"
    )
