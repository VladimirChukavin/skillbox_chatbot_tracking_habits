"""
Сервис обработки подтверждения удаления привычки.

Содержит функцию, которая вызывается при нажатии inline-кнопки
подтверждения удаления конкретной привычки или отмены действия.
Функция извлекает идентификатор привычки из callback-данных,
отправляет запрос на удаление через API-клиент и обновляет
сообщение с результатом.
"""

from telebot import TeleBot
from telebot.types import CallbackQuery
from loguru import logger

from bot.api.api_client import api_client


def show_confirm_delete_habit_choice(bot: TeleBot, call: CallbackQuery) -> None:
    """
    Обработать подтверждения удаления привычки или отмены
    действия.

    Извлекает идентификатор привычки из callback-данных формата
    "confirm_delete:<yes или no>". Отправляет запрос на удаление через
    API-клиент. При успешном удалении сбрасывает FSM-состояние
    пользователя и заменяет текст исходного сообщения на уведомление
    об успехе. При неудаче отправляет в чат сообщение об ошибке.
    При отмене действия отправляет сообщение, информирующее об
    отмене действия.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param call: Callback-запрос от inline-кнопки выбора привычки
    :type call: CallbackQuery
    :return: Ничего не возвращает
    :rtype: None
    """

    telegram_id = call.from_user.id
    chat_id = call.message.chat.id

    if call.data == "confirm_delete:no":
        bot.delete_state(telegram_id, chat_id)
        bot.answer_callback_query(call.id, "Удаление отменено.")
        return

    with bot.retrieve_data(telegram_id, chat_id) as data:
        habit_id = data.get("habit_id_to_delete")

    if not habit_id:
        bot.send_message(telegram_id, "Ошибка: не удалось определить привычку.")
        return

    result = api_client.delete_habit(telegram_id, habit_id)

    if result:
        bot.delete_state(telegram_id, call.message.chat.id)
        bot.edit_message_text(
            "✅ Привычка удалена.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )
        logger.info("Привычка {} удалена пользователем {}", habit_id, telegram_id)
    else:
        logger.error("Ошибка удаления привычки {}: {}", habit_id, result)
        bot.answer_callback_query(call.id, "❌ Не удалось удалить привычку.")
