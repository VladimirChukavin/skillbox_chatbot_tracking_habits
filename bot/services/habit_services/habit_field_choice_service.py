"""
Сервис обработки выбора поля привычки для редактирования.

Содержит функцию, которая вызывается при нажатии inline-кнопки
выбора конкретного поля привычки (название, описание, цель, срок)
или кнопки удаления. Функция определяет дальнейшее действие:
удаление привычки или переход к вводу нового значения поля.
"""

from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.states import EditHabitStates


def show_habit_field_choice(bot: TeleBot, call: CallbackQuery) -> None:
    """
    Обработать выбор поля привычки для редактирования.

    Извлекает название поля из callback-данных формата
    "field:<field_name>". Сохраняет выбранное поле в FSM-данных
    под ключом "editing_field", переводит пользователя в
    состояние ожидания ввода нового значения
    (EditHabitStates.waiting_for_new_value) и заменяет текст
    сообщения на запрос ввода с использованием человекочитаемой
    метки поля из словаря field_labels.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param call: Callback-запрос от inline-кнопки выбора поля
    :type call: CallbackQuery
    :return: Ничего не возвращает
    :rtype: None
    """

    telegram_id = call.from_user.id
    chat_id = call.message.chat.id
    parts = call.data.split(":")

    if len(parts) != 2 or parts[0] != "field":
        bot.answer_callback_query(call.id, "Ошибка: некорректная команда.")
        return

    field = parts[1]

    with bot.retrieve_data(telegram_id, chat_id) as data:
        data["editing_field"] = field

    bot.set_state(
        telegram_id,
        EditHabitStates.waiting_for_new_value,
        chat_id,
    )
    field_labels = {
        "title": "новое название",
        "description": "новое описание",
        "target_description": "новую цель",
        "target_days": "новый срок в днях",
    }
    bot.edit_message_text(
        f"Введите {field_labels.get(field, 'новое значение')}:",
        chat_id=chat_id,
        message_id=call.message.message_id,
    )
