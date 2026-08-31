"""
Сервис отображения списка привычек для отметки выполнения.

Содержит функцию, которая запрашивает у backend список привычек
пользователя и отображает inline-клавиатуру для выбора привычки.
Если список пуст — уведомляет пользователя.
"""

from telebot import TeleBot

from bot.api.api_client import api_client
from bot.keyboards.habits_keyboard import build_habits_keyboard
from bot.states import TrackHabitsStates


def show_track_habit(bot: TeleBot, telegram_id: int, chat_id: int) -> None:
    """
    Показать список привычек для отметки выполнения.

    Запрашивает список привычек пользователя через API-клиент.
    Если привычек нет — отправляет в чат уведомление об отсутствии
    активных элементов. Если список непустой — переводит
    пользователя в состояние ожидания выбора привычки
    (TrackHabitsStates.waiting_for_habit_choice) и отправляет
    inline-клавиатуру с префиксом callback-данных "track".

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param telegram_id: Идентификатор Telegram-пользователя
    :type telegram_id: int
    :param chat_id: Идентификатор чата, куда отправить сообщение
    :type chat_id: int
    :return: Ничего не возвращает
    :rtype: None
    """

    habits = api_client.list_habits(telegram_id)

    if not habits:
        bot.send_message(telegram_id, "❌ Нет активных привычек для отметки.")
        return

    bot.set_state(telegram_id, TrackHabitsStates.waiting_for_habit_choice, chat_id)

    keyboard = build_habits_keyboard(habits, "track", with_cancel=True)

    bot.send_message(
        chat_id,
        "Выберите привычку для отметки:",
        reply_markup=keyboard,
    )
