"""
Сервис отображения списка привычек для удаления.

Содержит функцию, которая запрашивает у backend список привычек
пользователя и отображает inline-клавиатуру для выбора удаляемой
привычки. Если список пуст — уведомляет пользователя.
"""

from telebot import TeleBot

from bot.api.api_client import api_client
from bot.keyboards.habits_keyboard import build_habits_keyboard
from bot.states import DeleteHabitsStates


def show_delete_habit(bot: TeleBot, telegram_id: int, chat_id: int) -> None:
    """
    Показать список привычек для удаления.

    Запрашивает список привычек пользователя через API-клиент.
    Если привычек нет — отправляет в чат уведомление об отсутствии
    удаляемых элементов. Если список непустой — переводит пользователя
    в состояние ожидания выбора привычки
    (DeleteHabitsStates.waiting_for_habit_choice) и отправляет
    inline-клавиатуру с префиксом callback-данных "delete".

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
        bot.send_message(chat_id, "❌ Нет привычек для удаления.")
        return

    bot.set_state(
        telegram_id,
        DeleteHabitsStates.waiting_for_habit_choice,
        chat_id,
    )

    bot.send_message(
        chat_id,
        "Выберите привычку:",
        reply_markup=build_habits_keyboard(habits, callback_prefix="delete"),
    )
