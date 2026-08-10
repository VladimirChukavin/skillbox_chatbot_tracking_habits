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


def build_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(text="➕ Добавить", callback_data="menu:add"),
        InlineKeyboardButton(text="📋 Список", callback_data="menu:list"),
    )
    keyboard.row(
        InlineKeyboardButton(text="✏️ Редактировать", callback_data="menu:edit"),
        InlineKeyboardButton(text="📊 Статистика", callback_data="menu:stats"),
    )
    keyboard.row(
        InlineKeyboardButton(text="✅ Отметить", callback_data="menu:track"),
        InlineKeyboardButton(text="⏰ Напоминание", callback_data="menu:reminder"),
    )

    return keyboard
