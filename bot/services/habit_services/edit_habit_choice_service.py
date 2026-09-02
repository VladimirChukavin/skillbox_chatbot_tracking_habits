"""
Сервис обработки выбора привычки для редактирования.

Содержит функцию, которая вызывается при нажатии inline-кнопки
редактирования конкретной привычки. Функция извлекает идентификатор
привычки из callback-данных, сохраняет его в FSM-данных и
отображает inline-клавиатуру для выбора редактируемого поля.
"""

from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.keyboards.edit_fields_keyboard import build_edit_fields_keyboard
from bot.states import EditHabitStates


def show_edit_habit_choice(bot: TeleBot, call: CallbackQuery) -> None:
    """
    Обработать выбор привычки для редактирования.

    Извлекает идентификатор привычки из callback-данных формата
    "edit:<habit_id>" и сохраняет его в данных состояния (FSM)
    под ключом "editing_habit_id". Переводит пользователя в
    состояние ожидания выбора поля
    (EditHabitStates.waiting_for_field_choice) и заменяет
    текст исходного сообщения на запрос «Что вы хотите изменить?»
    с inline-клавиатурой.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param call: Callback-запрос от inline-кнопки выбора привычки
    :type call: CallbackQuery
    :return: Ничего не возвращает
    :rtype: None
    """

    telegram_id = call.from_user.id
    chat_id = call.message.chat.id
    parts = call.data.split(":")

    if len(parts) != 2 or parts[0] != "edit":
        bot.answer_callback_query(call.id, "Ошибка: некорректная команда.")
        return

    habit_id = int(parts[1])

    with bot.retrieve_data(telegram_id, chat_id) as data:
        data["editing_habit_id"] = habit_id

    bot.set_state(
        telegram_id,
        EditHabitStates.waiting_for_field_choice,
        chat_id,
    )
    bot.edit_message_text(
        "Что вы хотите изменить?",
        chat_id=chat_id,
        message_id=call.message.message_id,
        reply_markup=build_edit_fields_keyboard(),
    )
