from telebot.handler_backends import State, StatesGroup


class RegistrationStates(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_password = State()


class AddHabitStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_target_description = State()
    waiting_for_target_days = State()


class EditHabitStates(StatesGroup):
    waiting_for_habit_choice = State()
    waiting_for_field_choice = State()
    waiting_for_new_value = State()


class TrackHabitsStates(StatesGroup):
    waiting_for_habit_choice = State()


class ReminderStates(StatesGroup):
    waiting_for_habit_choice = State()
    waiting_for_time = State()


class LoginStates(StatesGroup):
    waiting_for_password = State()
