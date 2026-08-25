"""
Сервис обработки выбора привычки для установки напоминания.

Содержит функцию, которая вызывается при нажатии inline-кнопки
выбора конкретной привычки. Функция извлекает идентификатор
привычки из callback-данных, сохраняет его в FSM-данных и
переводит пользователя к вводу времени напоминания.
"""

from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.states import ReminderStates


def show_reminder_choice(bot: TeleBot, call: CallbackQuery) -> None:
    """
    Обработать выбор привычки для установки напоминания.

    Извлекает идентификатор привычки из callback-данных формата
    "reminder:<habit_id>" и сохраняет его в данных состояния
    (FSM) под ключом "reminder_habit_id". Переводит
    пользователя в состояние ожидания ввода времени напоминания
    (ReminderStates.waiting_for_time) и заменяет текст
    исходного сообщения на запрос времени.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param call: Callback-запрос от inline-кнопки выбора привычки
    :type call: CallbackQuery
    :return: Ничего не возвращает
    :rtype: None
    """

    habit_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id

    with bot.retrieve_data(telegram_id, call.message.chat.id) as data:
        data["reminder_habit_id"] = habit_id

    bot.set_state(telegram_id, ReminderStates.waiting_for_time, call.message.chat.id)
    bot.edit_message_text(
        "Введите время напоминания в формате ЧЧ:ММ (например, 09:30):",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )
