from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_habits_keyboard(
    habits: list[dict], callback_prefix: str
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    for habit in habits:
        keyboard.add(
            InlineKeyboardButton(
                text=habit["title"],
                callback_data=f'{callback_prefix}:{habit["id"]}',
            )
        )

    return keyboard
