from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_edit_fields_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    fields = [
        ("Название", "field:title"),
        ("Описание", "field:description"),
        ("Цель", "field:target_description"),
        ("Срок (дней)", "field:target_days"),
        ("Удалить привычку", "field:delete"),
    ]

    for label, callback in fields:
        keyboard.add(InlineKeyboardButton(text=label, callback_data=callback))

    return keyboard
