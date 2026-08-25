"""
Сервис обработки выбора привычки для отметки выполнения.

Содержит функцию, которая вызывается при нажатии inline-кнопки
выбора привычки. Функция извлекает идентификатор привычки из
callback-данных и отображает inline-клавиатуру с кнопками
«Выполнено» и «Не выполнено» для отметки за текущий день.
"""

from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.keyboards.track_keyboard import build_track_keyboard


def show_track_choice(bot: TeleBot, call: CallbackQuery) -> None:
    """
    Обработать выбор привычки для отметки выполнения.

    Извлекает идентификатор привычки из callback-данных формата
    "track:<habit_id>" и заменяет текст исходного сообщения
    на запрос с inline-клавиатурой.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param call: Callback-запрос от inline-кнопки выбора привычки
    :type call: CallbackQuery
    :return: Ничего не возвращает
    :rtype: None
    """

    habit_id = int(call.data.split(":")[1])

    bot.edit_message_text(
        "Отметьте выполнение:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=build_track_keyboard(habit_id),
    )
