"""
Обработчики для установки напоминаний о привычках.

Содержит функцию регистрации хендлеров для команды /set_reminder,
выбора привычки (callback) и ввода времени напоминания (FSM состояние).
"""

from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from bot.services.reminder_services.set_reminder_service import show_set_reminder
from bot.services.reminder_services.reminder_choice_service import show_reminder_choice
from bot.services.reminder_services.reminder_time_service import show_reminder_time
from bot.states import ReminderStates


def register_reminder_handlers(bot: TeleBot) -> None:
    """
    Зарегистрировать обработчики для работы с напоминаниями.

    Связывает команду, callback-запросы и состояние (FSM) с
    соответствующими сервисными функциями.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :return: Ничего не возвращает
    :rtype: None
    """

    @bot.message_handler(commands=["set_reminder"])
    def handle_set_reminder(message: Message) -> None:
        """
        Обработчик команды /set_reminder. Начинает процесс установки напоминания.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_set_reminder(bot, message.from_user.id, message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("reminder:"))
    def handle_reminder_choice(call: CallbackQuery) -> None:
        """
        Обработчик выбора привычки для установки напоминания (callback "reminder:").

        :param call: Callback-запрос от inline-клавиатуры
        :type call: CallbackQuery
        :return: Ничего не возвращает
        :rtype: None
        """

        show_reminder_choice(bot, call)

    @bot.message_handler(state=ReminderStates.waiting_for_time)
    def handle_reminder_time(message: Message) -> None:
        """
        Обработчик состояния ожидания ввода времени напоминания.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_reminder_time(bot, message)
