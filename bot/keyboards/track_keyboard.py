from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_track_keyboard(habit_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(
            text="✅ Выполнено", callback_data=f"track_done:{habit_id}"
        ),
        InlineKeyboardButton(
            text="❌ Не выполнено", callback_data=f"track_skip:{habit_id}"
        ),
    )

    return keyboard
