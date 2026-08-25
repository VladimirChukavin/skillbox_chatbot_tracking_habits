"""
Сервис обработки выбора привычки для удаления.

Содержит функцию, которая вызывается при нажатии inline-кнопки
удаления конкретной привычки. Функция извлекает идентификатор
привычки из callback-данных, отправляет запрос на удаление
через API-клиент и обновляет сообщение с результатом.
"""

from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.api.api_client import api_client


def show_delete_habit_choice(bot: TeleBot, call: CallbackQuery) -> None:
    """
    Обработать выбор привычки для удаления.

    Извлекает идентификатор привычки из callback-данных формата
    "delete:<habit_id>". Отправляет запрос на удаление через
    API-клиент. При успешном удалении сбрасывает FSM-состояние
    пользователя и заменяет текст исходного сообщения на уведомление
    об успехе. При неудаче отправляет в чат сообщение об ошибке.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param call: Callback-запрос от inline-кнопки выбора привычки
    :type call: CallbackQuery
    :return: Ничего не возвращает
    :rtype: None
    """

    habit_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id

    if api_client.delete_habit(telegram_id, habit_id):
        bot.delete_state(telegram_id, call.message.chat.id)
        bot.edit_message_text(
            "🗑 Привычка удалена.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )
    else:
        bot.send_message(telegram_id, "❌ Не удалось удалить привычку.")
