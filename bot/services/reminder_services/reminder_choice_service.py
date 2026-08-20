from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.states import ReminderStates


def show_reminder_choice(bot: TeleBot, call: CallbackQuery) -> None:
    habit_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id

    with bot.retrieve_data(telegram_id, call.message.chat.id) as data:
        data["reminder_habit_id"] = habit_id

    bot.set_state(telegram_id, ReminderStates.waiting_for_time, call.message.chat.id)
    bot.edit_message_text(
        "Введите время напоминания в формате ЧЧ:ММ (например, 09:30):",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )
