"""
Сервис обработки выбора поля привычки для редактирования.

Содержит функцию, которая вызывается при нажатии inline-кнопки
выбора конкретного поля привычки (название, описание, цель, срок)
или кнопки удаления. Функция определяет дальнейшее действие:
удаление привычки или переход к вводу нового значения поля.
"""

from telebot import TeleBot
from telebot.types import CallbackQuery

from bot.api.api_client import api_client
from bot.states import EditHabitStates


def show_habit_field_choice(bot: TeleBot, call: CallbackQuery) -> None:
    """
    Обработать выбор поля привычки для редактирования.

    Извлекает название поля из callback-данных формата
    "field:<field_name>". Если выбрано поле "delete" —
    извлекает идентификатор редактируемой привычки из FSM-данных
    (ключ "editing_habit_id") и отправляет запрос на удаление
    через API-клиент. При успехе сбрасывает FSM-состояние и
    заменяет текст сообщения на уведомление об удалении, при
    неудаче — отправляет сообщение об ошибке.

    Для остальных полей сохраняет выбранное поле в FSM-данных
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

    field = call.data.split(":")[1]
    telegram_id = call.from_user.id

    with bot.retrieve_data(telegram_id, call.message.chat.id) as data:
        data["editing_field"] = field

    bot.set_state(
        telegram_id,
        EditHabitStates.waiting_for_new_value,
        call.message.chat.id,
    )
    field_labels = {
        "title": "новое название",
        "description": "новое описание",
        "target_description": "новую цель",
        "target_days": "новый срок в днях",
    }
    bot.edit_message_text(
        f"Введите {field_labels.get(field, 'новое значение')}:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )
