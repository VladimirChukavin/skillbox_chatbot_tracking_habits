"""
Сервис обработки ввода названия привычки.

Содержит функцию, которая валидирует введённое название, сохраняет
его в данных состояния (FSM) и переводит пользователя к следующему
шагу формы создания привычки — вводу описания.
"""

from telebot.types import Message
from telebot import TeleBot

from bot.states import AddHabitStates


def show_habit_title(bot: TeleBot, message: Message) -> None:
    """
    Обработать ввод названия привычки.

    Проверяет, что название не пустое. Если введён пустой текст —
    отправляет уведомление и прерывает обработку без изменения
    состояния. При непустом значении сохраняет название в данных
    состояния (FSM) под ключом "title" и переводит пользователя
    в состояние ожидания ввода описания
    (AddHabitStates.waiting_for_description), отправляя
    соответствующее сообщение.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param message: Входящее сообщение с названием привычки
    :type message: Message
    :return: Ничего не возвращает
    :rtype: None
    """

    title = message.text.strip() if message.text else ""

    if not title:
        bot.send_message(message.from_user.id, "Название не может быть пустым:")
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["title"] = title

    bot.set_state(
        message.from_user.id,
        AddHabitStates.waiting_for_description,
        message.chat.id,
    )
    bot.send_message(
        message.from_user.id, "Введите описание (или '-' чтобы пропустить):"
    )
