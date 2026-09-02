"""
Определение FSM-состояний бота.

Содержит группы состояний, используемые для управления
диалогами пользователя через конечный автомат (FSM).
Каждая группа соответствует определённому сценарию: регистрация,
добавление, редактирование, удаление, отметка привычек, установка
напоминаний и вход в систему.
"""

from telebot.handler_backends import State, StatesGroup


class RegistrationStates(StatesGroup):
    """
    Состояния процесса регистрации нового пользователя.

    :param waiting_for_full_name: Ожидание ввода полного имени
    :param waiting_for_password: Ожидание ввода пароля
    """

    waiting_for_full_name = State()
    waiting_for_password = State()


class AddHabitStates(StatesGroup):
    """
    Состояния формы добавления привычки.

    :param waiting_for_title: Ожидание ввода названия
    :param waiting_for_description: Ожидание ввода описания
    :param waiting_for_target_description: Ожидание ввода цели
    :param waiting_for_target_days: Ожидание ввода срока в днях
    """

    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_target_description = State()
    waiting_for_target_days = State()


class EditHabitStates(StatesGroup):
    """
    Состояния процесса редактирования привычки.

    :param waiting_for_habit_choice: Ожидание выбора привычки
    :param waiting_for_field_choice: Ожидание выбора поля для редактирования
    :param waiting_for_new_value: Ожидание ввода нового значения
    """

    waiting_for_habit_choice = State()
    waiting_for_field_choice = State()
    waiting_for_new_value = State()


class TrackHabitsStates(StatesGroup):
    """
    Состояния процесса отметки выполнения привычки.

    :param waiting_for_habit_choice: Ожидание выбора привычки для отметки
    """

    waiting_for_habit_choice = State()


class ReminderStates(StatesGroup):
    """
    Состояния процесса установки напоминания.

    :param waiting_for_habit_choice: Ожидание выбора привычки
    :param waiting_for_time: Ожидание ввода времени в формате ЧЧ:ММ
    """

    waiting_for_habit_choice = State()
    waiting_for_time = State()


class LoginStates(StatesGroup):
    """
    Состояния процесса входа в систему (логин).

    :param waiting_for_password: Ожидание ввода пароля
    """

    waiting_for_password = State()


class DeleteHabitsStates(StatesGroup):
    """
    Состояния процесса удаления привычки.

    :param waiting_for_habit_choice: Ожидание выбора удаляемой привычки
    """

    waiting_for_habit_choice = State()
    waiting_for_deletion_confirmation = State()


class StatsStates(StatesGroup):
    """
    Состояния процесса вывода статистики.

    :param waiting_for_habit_choice: Ожидание выбора привычки
    """

    waiting_for_habit_choice = State()
