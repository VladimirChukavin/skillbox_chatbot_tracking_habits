"""
Обработчики сообщений, состояний и callback-запросов для управления привычками.

Содержит функцию регистрации хендлеров для команд (добавление, список,
редактирование, удаление), состояний FSM (ввод данных) и навигации
по inline-меню.
"""

from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from bot.services.habit_services.add_habit_service import show_add_habit
from bot.services.habit_services.confirm_delete_habit_service import (
    show_confirm_delete_habit_choice,
)
from bot.services.habit_services.delete_habit_choice_service import (
    show_delete_habit_choice,
)
from bot.services.habit_services.delete_habit_service import show_delete_habit
from bot.services.habit_services.habit_title_service import show_habit_title
from bot.services.habit_services.habit_description_service import show_habit_description
from bot.services.habit_services.habit_target_service import show_habit_target
from bot.services.habit_services.habit_target_days_service import show_habit_target_days
from bot.services.habit_services.habits_list_service import show_habits_list
from bot.services.habit_services.edit_habit_service import show_edit_habit
from bot.services.habit_services.edit_habit_choice_service import show_edit_habit_choice
from bot.services.habit_services.habit_field_choice_service import (
    show_habit_field_choice,
)
from bot.services.habit_services.habit_new_value_service import show_habit_new_value
from bot.services.habit_services.habit_menu_navigation_service import (
    show_habit_menu_navigation,
)
from bot.states import AddHabitStates, EditHabitStates


def register_habit_handlers(bot: TeleBot) -> None:
    """
    Зарегистрировать обработчики для управления привычками.

    Связывает команды, состояния (FSM) и callback-запросы inline-клавиатур
    с соответствующими сервисными функциями.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :return: Ничего не возвращает
    :rtype: None
    """

    @bot.message_handler(commands=["add_habit"])
    def handle_add_habit(message: Message) -> None:
        """
        Обработчик команды /add_habit. Начинает процесс добавления привычки.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_add_habit(bot, message.from_user.id, message.chat.id)

    @bot.message_handler(state=AddHabitStates.waiting_for_title)
    def handle_habit_title(message: Message) -> None:
        """
        Обработчик состояния ожидания названия привычки.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_habit_title(bot, message)

    @bot.message_handler(state=AddHabitStates.waiting_for_description)
    def handle_habit_description(message: Message) -> None:
        """
        Обработчик состояния ожидания описания привычки.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_habit_description(bot, message)

    @bot.message_handler(state=AddHabitStates.waiting_for_target_description)
    def handle_habit_target(message: Message) -> None:
        """
        Обработчик состояния ожидания цели привычки.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_habit_target(bot, message)

    @bot.message_handler(state=AddHabitStates.waiting_for_target_days)
    def handle_habit_target_days(message: Message) -> None:
        """
        Обработчик состояния ожидания срока выполнения в днях.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_habit_target_days(bot, message)

    @bot.message_handler(commands=["habits"])
    def handle_list_habits(message: Message) -> None:
        """
        Обработчик команды /habits. Показывает список привычек.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_habits_list(bot, message.from_user.id, message.chat.id)

    @bot.message_handler(commands=["edit_habit"])
    def handle_edit_habit(message: Message) -> None:
        """
        Обработчик команды /edit_habit. Начинает процесс редактирования.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_edit_habit(bot, message.from_user.id, message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("edit:"))
    def handle_edit_habit_choice(call: CallbackQuery) -> None:
        """
        Обработчик выбора привычки для редактирования (callback "edit:").

        :param call: Callback-запрос от inline-клавиатуры
        :type call: CallbackQuery
        :return: Ничего не возвращает
        :rtype: None
        """

        show_edit_habit_choice(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("field:"))
    def handle_habit_field_choice(call: CallbackQuery) -> None:
        """
        Обработчик выбора поля привычки для редактирования (callback "field:").

        :param call: Callback-запрос от inline-клавиатуры
        :type call: CallbackQuery
        :return: Ничего не возвращает
        :rtype: None
        """

        show_habit_field_choice(bot, call)

    @bot.message_handler(state=EditHabitStates.waiting_for_new_value)
    def handle_habit_new_value(message: Message) -> None:
        """
        Обработчик состояния ожидания нового значения для поля привычки.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_habit_new_value(bot, message)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("menu:"))
    def handle_menu_navigation(call: CallbackQuery) -> None:
        """
        Обработчик навигации по главному меню (callback "menu:").

        :param call: Callback-запрос от inline-клавиатуры
        :type call: CallbackQuery
        :return: Ничего не возвращает
        :rtype: None
        """

        show_habit_menu_navigation(bot, call)

    @bot.message_handler(commands=["delete_habit"])
    def handle_delete_habit(message: Message) -> None:
        """
        Обработчик команды /delete_habit. Начинает процесс удаления.

        :param message: Входящее сообщение от пользователя
        :type message: Message
        :return: Ничего не возвращает
        :rtype: None
        """

        show_delete_habit(bot, message.from_user.id, message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("delete:"))
    def handle_delete_habit_choice(call: CallbackQuery) -> None:
        """
        Обработчик выбора привычки для удаления (callback "delete:").

        :param call: Callback-запрос от inline-клавиатуры
        :type call: CallbackQuery
        :return: Ничего не возвращает
        :rtype: None
        """

        show_delete_habit_choice(bot, call)

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("confirm_delete:")
    )
    def handle_confirm_delete_habit(call: CallbackQuery) -> None:
        """
        Обработчик выбора подтверждения удаления
        привычки (callback "confirm_delete:").

        :param call: Callback-запрос от inline-клавиатуры
        :type call: CallbackQuery
        :return: Ничего не возвращает
        :rtype: None
        """

        show_confirm_delete_habit_choice(bot, call)
