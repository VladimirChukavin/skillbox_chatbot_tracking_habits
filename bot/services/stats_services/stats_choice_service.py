"""
Сервис отображения статистики по выбранной привычке.

Содержит функцию, которая вызывается при нажатии inline-кнопки
выбора привычки. Функция извлекает идентификатор привычки из
callback-данных, запрашивает статистику через API-клиент и
формирует читаемое текстовое сообщение с прогрессом выполнения.
"""

from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.api.api_client import api_client


def show_stats_choice(bot: TeleBot, call: CallbackQuery) -> None:
    """
    Обработать выбор привычки для просмотра статистики.

    Извлекает идентификатор привычки из callback-данных формата
    "stats:<habit_id>" и запрашивает статистику через
    api_client.get_habit_stats. Если запрос вернул None —
    отвечает на callback уведомлением об ошибке и прерывает
    обработку.

    При успехе формирует текстовое сообщение, содержащее название
    привычки, количество выполненных дней из целевого, процент
    прогресса и отметку о выполнении за сегодня.
    Заменяет текст исходного сообщения на сформированное.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param call: Callback-запрос от inline-кнопки выбора привычки
    :type call: CallbackQuery
    :return: Ничего не возвращает
    :rtype: None
    """

    telegram_id = call.from_user.id
    parts = call.data.split(":")

    if len(parts) != 2 or parts[0] != "stats":
        bot.answer_callback_query(call.id, "❌ Ошибка: некорректная команда.")
        return

    habit_id = int(parts[1])

    stats = api_client.get_habit_stats(telegram_id, habit_id)

    if stats is None:
        bot.answer_callback_query(call.id, "❌ Ошибка: не удалось получить статистику.")
        return

    today_mark = (
        "✅ выполнена сегодня"
        if stats["is_completed_today"]
        else "⬜ не отмечена сегодня"
    )
    text = (
        f"Статистика по привычке \"{stats['title']}\"\n\n"
        f"Выполнено: {stats['completed_count']} из {stats['target_days']} дней\n"
        f"Прогресс: {stats['progress_percent']}%\n"
        f"Сегодня: {today_mark}"
    )
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )
