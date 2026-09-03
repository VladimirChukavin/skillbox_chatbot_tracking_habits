"""
Сервис отметки невыполнения привычки.

Содержит функцию, которая вызывается при нажатии inline-кнопки
«Не выполнено». Функция извлекает идентификатор привычки из
callback-данных, отправляет запрос на отметку невыполнения через
API-клиент, сбрасывает FSM-состояние и обновляет сообщение
с результатом.
"""

from loguru import logger
from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.api.api_client import api_client


def show_track_skip(bot: TeleBot, call: CallbackQuery) -> None:
    """
    Обработать отметку привычки как невыполненной.

    Извлекает идентификатор привычки из callback-данных формата
    "track_skip:<habit_id>" и отправляет запрос на отметку
    через api_client.track_habit с параметром
    is_completed=False. Сбрасывает FSM-состояние пользователя.

    Если запрос вернул None — заменяет текст исходного сообщения
    на уведомление об ошибке и прерывает обработку. При успехе
    заменяет текст сообщения на уведомление о невыполнении с
    переносом привычки на следующий день.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param call: Callback-запрос от inline-кнопки «Не выполнено»
    :type call: CallbackQuery
    :return: Ничего не возвращает
    :rtype: None
    """

    telegram_id = call.from_user.id
    chat_id = call.message.chat.id

    parts = call.data.split(":")

    if len(parts) != 2 or parts[0] != "track_skip":
        bot.answer_callback_query(call.id, "❌ Ошибка: некорректная команда.")
        return

    habit_id = int(parts[1])

    result = None
    try:
        result = api_client.track_habit(telegram_id, habit_id, is_completed=False)
    except Exception as error:
        logger.error("Ошибка при отметке невыполнения привычки {}: {}", habit_id, error)
        bot.answer_callback_query(call.id, "❌ Ошибка при отметке. Попробуйте позже.")
        return

    if result is None:
        bot.edit_message_text(
            "❌ Ошибка при отметке.",
            chat_id=chat_id,
            message_id=call.message.message_id,
        )
        return

    logger.info("Привычка {} пропущена пользователем {}", habit_id, telegram_id)

    bot.edit_message_text(
        "✅ Отмечено как невыполненное. Привычка переносится на завтра.",
        chat_id=chat_id,
        message_id=call.message.message_id,
    )

    bot.delete_state(telegram_id, chat_id)
    bot.answer_callback_query(call.id)
