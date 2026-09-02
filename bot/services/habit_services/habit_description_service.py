"""
Сервис обработки ввода описания привычки.

Содержит функцию, которая сохраняет введённое описание в данных
состояния (FSM) и переводит пользователя к следующему шагу
формы создания привычки — вводу цели.
"""

from telebot import TeleBot
from telebot.types import Message

from bot.states import AddHabitStates


def show_habit_description(bot: TeleBot, message: Message) -> None:
    """
    Обработать ввод описания привычки.

    Извлекает текст описания из сообщения и сохраняет его в данных
    состояния (FSM) под ключом "description". Если пользователь
    ввёл "-" (пропуск), в FSM сохраняется None. Переводит
    пользователя в состояние ожидания ввода цели привычки
    (AddHabitStates.waiting_for_target_description) и отправляет
    соответствующее сообщение с подсказкой о возможности пропуска.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param message: Входящее сообщение с описанием привычки
    :type message: Message
    :return: Ничего не возвращает
    :rtype: None
    """

    description = message.text.strip() if message.text else ""

    if description and description != "-":
        if len(description) > 500:
            bot.send_message(
                message.from_user.id,
                "⚠️ Описание слишком длинное. Максимальная длина 500 символов."
                "Попробуйте ещё раз:",
            )
            return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["description"] = None if description == "-" else description

    bot.set_state(
        message.from_user.id,
        AddHabitStates.waiting_for_target_description,
        message.chat.id,
    )
    bot.send_message(
        message.from_user.id, "Введите цель привычки (или '-' чтобы пропустить):"
    )
