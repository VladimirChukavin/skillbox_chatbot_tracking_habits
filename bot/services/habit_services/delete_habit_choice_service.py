"""
Сервис обработки подтверждения удаления привычки.

Содержит функцию, которая вызывается при нажатии inline-кнопки
удаления конкретной привычки. Функция извлекает идентификатор
привычки из callback-данных, отправляет запрос на подтверждение
удаление через API-клиент и обновляет сообщение с результатом.
"""

from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.api.api_client import api_client
from bot.keyboards.delete_confirmation_keyboard import (
    build_delete_confirmation_keyboard,
)
from bot.states import DeleteHabitsStates


def show_delete_habit_choice(bot: TeleBot, call: CallbackQuery) -> None:
    """
    Обработать подтверждение удаления привычки.

    Извлекает идентификатор привычки из callback-данных формата
    "delete:<habit_id>". Отправляет запрос на подтверждение удаления
    через API-клиент. При этом выводит текст сообщения для подтверждения
    удаления или отмены действия. Также выводит клавиатуру с кнопками
    выбора - подтвердить или отменить действие.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param call: Callback-запрос от inline-кнопки выбора привычки
    :type call: CallbackQuery
    :return: Ничего не возвращает
    :rtype: None
    """

    habit_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id
    chat_id = call.message.chat.id
    habit_data = api_client.get_habit(telegram_id, habit_id)

    if habit_data is None:
        bot.send_message(telegram_id, "❌ Привычка не найдена или произошла ошибка")
        return

    habit_title = habit_data.get("title", f"Привычка #{habit_id}")

    with bot.retrieve_data(telegram_id, chat_id) as data:
        data["habit_id_to_delete"] = habit_id

    bot.set_state(
        telegram_id,
        DeleteHabitsStates.waiting_for_deletion_confirmation,
        chat_id,
    )

    bot.edit_message_text(
        f'Вы уверены, что хотите удалить привычку "{habit_title}"?',
        chat_id=chat_id,
        message_id=call.message.message_id,
        reply_markup=build_delete_confirmation_keyboard(),
    )
