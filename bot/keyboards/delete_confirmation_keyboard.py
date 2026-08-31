"""
Клавиатура для подтверждения удаления привычки или отмены.

Содержит функцию для построения inline-клавиатуры, позволяющей
пользователю подтвердить удаление привычки или отменить действие.
"""

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_delete_confirmation_keyboard() -> InlineKeyboardMarkup:
    """
    Построить клавиатуру для подтверждения удаления
    привычки или отмены действия.

    Создаёт кнопки для подтверждения удаления и
    отмены действия.

    :return: Объект inline-клавиатуры с кнопками полей
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(text="✅ Да, удалить", callback_data="confirm_delete:yes"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="confirm_delete:no"),
    )
    return keyboard
