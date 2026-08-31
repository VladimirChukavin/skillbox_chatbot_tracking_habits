"""
Динамическая клавиатура для отображения списка привычек.

Содержит функцию для построения inline-клавиатуры на основе переданного
списка привычек с использованием заданного префикса для callback-данных.
"""

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_habits_keyboard(
    habits: list[dict], callback_prefix: str, with_cancel: bool = False
) -> InlineKeyboardMarkup:
    """
    Построить inline-клавиатуру из списка привычек.

    Создаёт по одной кнопке для каждой привычки. Текст кнопки — название
    привычки, callback_data формируется в формате <prefix>:<habit_id>.

    :param habits: Список словарей с данными привычек (должны содержать id и title)
    :type habits: list[dict]
    :param callback_prefix: Префикс для callback_data (например, "edit", "delete", "track")
    :type callback_prefix: str
    :param with_cancel: Признак включения кнопки "Отмена" в клавиатуре
    :type with_cancel: bool
    :return: Объект inline-клавиатуры со списком привычек
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()

    for habit in habits:
        keyboard.add(
            InlineKeyboardButton(
                text=habit["title"],
                callback_data=f'{callback_prefix}:{habit["id"]}',
            )
        )

    if with_cancel:
        keyboard.row(InlineKeyboardButton(text="❌ Отмена", callback_data="cancel"))

    return keyboard
