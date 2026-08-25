"""
Inline-клавиатура главного меню бота.

Содержит функцию для построения главного меню управления привычками
(добавление, список, редактирование, статистика, отметка, напоминания, удаление).
"""

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Построить клавиатуру главного меню.

    Создаёт сетку кнопок для основных действий с привычками.
    Callback-данные начинаются с префикса "menu:".

    :return: Объект inline-клавиатуры главного меню
    :rtype: InlineKeyboardMarkup
    """

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
    keyboard.row(InlineKeyboardButton(text="❌ Удалить", callback_data="menu:delete"))

    return keyboard
