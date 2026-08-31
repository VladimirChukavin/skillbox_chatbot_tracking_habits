"""
Обработчики для получения статистики по привычкам.

Содержит функцию регистрации хендлеров для команды /habit_stats
и выбора конкретной привычки (callback) для отображения её прогресса.
"""

from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from bot.services.cancel_service import show_cancel
from bot.services.stats_services.habit_stats_service import show_habit_stats
from bot.services.stats_services.stats_choice_service import show_stats_choice


def register_stats_handler(bot: TeleBot) -> None:
    """
    Зарегистрировать обработчики для просмотра статистики.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :return: Ничего не возвращает
    :rtype: None
    """

    @bot.message_handler(commands=["habit_stats"])
    def handle_habit_stats(message: Message) -> None:
        """
        Обработчик команды /habit_stats. Показывает список привычек для выбора.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_habit_stats(bot, message.from_user.id, message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("stats:"))
    def handle_stats_choice(call: CallbackQuery) -> None:
        """
        Обработчик выбора привычки для просмотра статистики (callback "stats:").

        :param call: Callback-запрос от inline-клавиатуры
        :type call: CallbackQuery
        :return: Ничего не возвращает
        :rtype: None
        """

        show_stats_choice(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("cancel"))
    def handle_stats_cancel(call: CallbackQuery) -> None:
        """
        Обработчик отмены просмотра статистики (callback "cancel").

        :param call: Callback-запрос от inline-клавиатуры
        :type call: CallbackQuery
        :return: Ничего не возвращает
        :rtype: None
        """

        show_cancel(bot, call)
