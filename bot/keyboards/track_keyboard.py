"""
Inline-клавиатура для отметки выполнения привычки.

Содержит функцию для построения клавиатуры с кнопками "Выполнено"
и "Не выполнено" для трекинга привычек.
"""

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_track_keyboard(habit_id: int) -> InlineKeyboardMarkup:
    """
    Построить клавиатуру для отметки выполнения привычки.

    Создаёт две кнопки в одной строке: для отметки выполнения
    (callback "track_done:") и невыполнения (callback "track_skip:").
    В callback_data передаётся ID привычки.

    :param habit_id: Идентификатор привычки для отметки
    :type habit_id: int
    :return: Объект inline-клавиатуры с кнопками отметки
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(
            text="✅ Выполнено", callback_data=f"track_done:{habit_id}"
        ),
        InlineKeyboardButton(
            text="✖️ Не выполнено", callback_data=f"track_skip:{habit_id}"
        ),
    )
    keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data="cancel"))

    return keyboard
