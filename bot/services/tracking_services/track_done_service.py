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

    habit_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id
    result = api_client.track_habit(telegram_id, habit_id, is_completed=True)
    bot.delete_state(telegram_id, call.message.chat.id)

    if result is None:
        bot.answer_callback_query(call.id, "Ошибка при отметке")
        return

    progress = f"{result['completed_count']}/{result['target_days']}"
    bot.edit_message_text(
        f"✅ Отмечено как выполненное! Прогресс: {progress}",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )
    logger.bind(sent_message=True).info(
        "Привычка {} отмечена выполненной пользователем {}", habit_id, telegram_id
    )
