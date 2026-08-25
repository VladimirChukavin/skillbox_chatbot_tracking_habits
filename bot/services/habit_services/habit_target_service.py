"""
Сервис обработки ввода цели привычки.

Содержит функцию, которая сохраняет введённую цель в данных
состояния (FSM) и переводит пользователя к следующему шагу
формы создания привычки — вводу срока выполнения в днях.
"""

from telebot import TeleBot
from telebot.types import Message

from bot.states import AddHabitStates


def show_habit_target(bot: TeleBot, message: Message) -> None:
    """
    Обработать ввод цели привычки.

    Извлекает текст цели из сообщения и сохраняет его в данных
    состояния (FSM) под ключом "target_description". Если
    пользователь ввёл "-" (пропуск), в FSM сохраняется None.
    Переводит пользователя в состояние ожидания ввода срока
    выполнения в днях (AddHabitStates.waiting_for_target_days)
    и отправляет соответствующее сообщение.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param message: Входящее сообщение с целью привычки
    :type message: Message
    :return: Ничего не возвращает
    :rtype: None
    """

    target_description = message.text.strip() if message.text else ""

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["target_description"] = (
            None if target_description == "-" else target_description
        )

    bot.set_state(
        message.from_user.id,
        AddHabitStates.waiting_for_target_days,
        message.chat.id,
    )
    bot.send_message(
        message.from_user.id, "Введите срок выполнения в днях (по умолчанию 21):"
    )
