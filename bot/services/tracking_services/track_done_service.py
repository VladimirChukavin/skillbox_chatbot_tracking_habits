"""
Сервис отметки выполнения привычки.

Содержит функцию, которая вызывается при нажатии inline-кнопки
«Выполнено». Функция извлекает идентификатор привычки из
callback-данных, отправляет запрос на отметку выполнения через
API-клиент, сбрасывает FSM-состояние и обновляет сообщение
с прогрессом.
"""

from loguru import logger
from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.api.api_client import api_client


def show_track_done(bot: TeleBot, call: CallbackQuery) -> None:
    """
    Обработать отметку привычки как выполненной.

    Извлекает идентификатор привычки из callback-данных формата
    "track_done:<habit_id>" и отправляет запрос на отметку
    выполнения через api_client.track_habit с параметром
    is_completed=True. Сбрасывает FSM-состояние пользователя.

    Если запрос вернул None — отвечает на callback уведомлением
    об ошибке и прерывает обработку. При успехе формирует строку
    прогресса в формате completed_count/target_days, заменяет
    текст исходного сообщения на уведомление с прогрессом и
    записывает событие в лог через loguru.logger.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param call: Callback-запрос от inline-кнопки «Выполнено»
    :type call: CallbackQuery
    :return: Ничего не возвращает
    :rtype: None
    """

    telegram_id = call.from_user.id
    chat_id = call.message.chat.id

    parts = call.data.split(":")

    if len(parts) != 2 or parts[0] != "track_done":
        bot.answer_callback_query(call.id, "❌ Ошибка: некорректная команда.")
        return

    habit_id = int(parts[1])

    result = api_client.track_habit(telegram_id, habit_id, is_completed=True)

    if result is None:
        bot.answer_callback_query(call.id, "❌ Ошибка при отметке")
        return

    bot.delete_state(telegram_id, chat_id)

    progress = f"{result['completed_count']}/{result['target_days']}"
    bot.edit_message_text(
        f"✅ Отмечено как выполненное! Прогресс: {progress}",
        chat_id=chat_id,
        message_id=call.message.message_id,
    )
    logger.bind(sent_message=True).info(
        "Привычка {} отмечена выполненной пользователем {}", habit_id, telegram_id
    )
