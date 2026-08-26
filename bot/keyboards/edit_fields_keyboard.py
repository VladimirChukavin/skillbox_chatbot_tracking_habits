"""
Клавиатура для выбора поля привычки при редактировании.

Содержит функцию для построения inline-клавиатуры, позволяющей
пользователю выбрать, какое поле привычки обновить или удалить её.
"""

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_edit_fields_keyboard() -> InlineKeyboardMarkup:
    """
    Построить клавиатуру выбора поля для редактирования привычки.

    Создаёт кнопки для обновления названия, описания, цели, срока,
    а также для полного удаления привычки.

    :return: Объект inline-клавиатуры с кнопками полей
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()
    fields = [
        ("Название", "field:title"),
        ("Описание", "field:description"),
        ("Цель", "field:target_description"),
        ("Срок (дней)", "field:target_days"),
    ]

    for label, callback in fields:
        keyboard.add(InlineKeyboardButton(text=label, callback_data=callback))

    return keyboard
