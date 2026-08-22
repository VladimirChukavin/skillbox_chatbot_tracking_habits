from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.keyboards.edit_fields_keyboard import build_edit_fields_keyboard
from bot.states import EditHabitStates


def show_edit_habit_choice(bot: TeleBot, call: CallbackQuery) -> None:
    habit_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id

    with bot.retrieve_data(telegram_id, call.message.chat.id) as data:
        data["editing_habit_id"] = habit_id

    bot.set_state(
        telegram_id,
        EditHabitStates.waiting_for_field_choice,
        call.message.chat.id,
    )
    bot.edit_message_text(
        "Что вы хотите изменить?",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=build_edit_fields_keyboard(),
    )
