from telebot.types import Message
from telebot import TeleBot

from bot.states import AddHabitStates


def show_habit_title(bot: TeleBot, message: Message) -> None:
    title = message.text.strip() if message.text else ""

    if not title:
        bot.send_message(message.from_user.id, "Название не может быть пустым:")
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["title"] = title

    bot.set_state(
        message.from_user.id,
        AddHabitStates.waiting_for_description,
        message.chat.id,
    )
    bot.send_message(
        message.from_user.id, "Введите описание (или '-' чтобы пропустить):"
    )
