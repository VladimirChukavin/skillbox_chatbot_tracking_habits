"""
Обработчики для отметки выполнения привычек (трекинг).

Содержит функцию регистрации хендлеров для команды /track_habit,
выбора привычки и отметки её выполнения/невыполнения через callback-кнопки.
"""

from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from bot.services.cancel_service import show_cancel
from bot.services.tracking_services.track_habit_service import show_track_habit
from bot.services.tracking_services.track_choice_service import show_track_choice
from bot.services.tracking_services.track_done_service import show_track_done
from bot.services.tracking_services.track_skip_service import show_track_skip


def register_tracking_handlers(bot: TeleBot) -> None:
    """
    Зарегистрировать обработчики для трекинга выполнения привычек.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :return: Ничего не возвращает
    :rtype: None
    """

    @bot.message_handler(commands=["track_habit"])
    def handle_track_habit(message: Message) -> None:
        """
        Обработчик команды /track_habit. Показывает список привычек для отметки.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_track_habit(bot, message.from_user.id, message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("track:"))
    def handle_track_choice(call: CallbackQuery) -> None:
        """
        Обработчик выбора привычки для отметки (callback "track:").

        :param call: Callback-запрос от inline-клавиатуры
        :type call: CallbackQuery
        :return: Ничего не возвращает
        :rtype: None
        """

        show_track_choice(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("track_done:"))
    def handle_track_done(call: CallbackQuery) -> None:
        """
        Обработчик отметки выполнения привычки (callback "track_done:").

        :param call: Callback-запрос от inline-клавиатуры
        :type call: CallbackQuery
        :return: Ничего не возвращает
        :rtype: None
        """

        show_track_done(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("track_skip:"))
    def handle_track_skip(call: CallbackQuery) -> None:
        """
        Обработчик отметки невыполнения привычки (callback "track_skip:").

        :param call: Callback-запрос от inline-клавиатуры
        :type call: CallbackQuery
        :return: Ничего не возвращает
        :rtype: None
        """

        show_track_skip(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("cancel"))
    def handle_track_cancel(call: CallbackQuery) -> None:
        """
        Обработчик отмены трекинга выполнения привычек (callback "cancel").

        :param call: Callback-запрос от inline-клавиатуры
        :type call: CallbackQuery
        :return: Ничего не возвращает
        :rtype: None
        """

        show_cancel(bot, call)
