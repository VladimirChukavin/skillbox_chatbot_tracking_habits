"""
Сервис отображения списка привычек для просмотра статистики.

Содержит функцию, которая запрашивает у backend список привычек
пользователя и отображает inline-клавиатуру для выбора привычки.
Если список пуст — уведомляет пользователя.
"""

from loguru import logger
from telebot import TeleBot

from bot.api.api_client import api_client
from bot.keyboards.habits_keyboard import build_habits_keyboard
from bot.states import StatsStates


def show_habit_stats(bot: TeleBot, telegram_id: int, chat_id: int) -> None:
    """
    Показать список привычек для просмотра статистики.

    Запрашивает список привычек пользователя через API-клиент.
    Если привычек нет — отправляет в чат уведомление об отсутствии
    доступных элементов. Если список непустой — отправляет
    inline-клавиатуру с префиксом callback-данных "stats",
    для выбора привычки, по которой требуется показать статистику.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param telegram_id: Идентификатор Telegram-пользователя
    :type telegram_id: int
    :param chat_id: Идентификатор чата, куда отправить сообщение
    :type chat_id: int
    :return: Ничего не возвращает
    :rtype: None
    """

    try:
        habits = api_client.list_habits(telegram_id)
    except Exception as error:
        logger.error(
            "Ошибка при получении списка привычек (telegram_id={}): {}",
            telegram_id,
            error,
        )
        bot.send_message(
            chat_id, "❌ Ошибка при получении списка привычек. Попробуйте позже."
        )
        return

    if not habits:
        bot.send_message(telegram_id, "❌ Нет привычек для просмотра статистики.")
        return

    bot.set_state(telegram_id, StatsStates.waiting_for_habit_choice, chat_id)

    keyboard = build_habits_keyboard(habits, "stats", with_cancel=True)

    bot.send_message(
        telegram_id,
        "Выберите привычку:",
        reply_markup=keyboard,
    )
