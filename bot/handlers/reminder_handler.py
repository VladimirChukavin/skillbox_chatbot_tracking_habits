from telebot import TeleBot
from telebot.types import Message
from loguru import logger

from bot.api_client import api_client
from bot.keyboards import build_habits_keyboard
from bot.states import ReminderStates


def register_reminder_handlers(bot: TeleBot) -> None:
    @bot.message_handler(commands=["set_reminder"])
    def handle_set_reminder(message: Message) -> None:
        telegram_id = message.from_user.id
        habits = api_client.list_habits(telegram_id)

        if not habits:
            bot.send_message(telegram_id, "Нет привычек для установки напоминания.")
            return

        bot.set_state(
            telegram_id, ReminderStates.waiting_for_habit_choice, message.chat.id
        )
        keyboard = build_habits_keyboard(habits, callback_prefix="reminder")
        bot.send_message(telegram_id, "Выберите привычку:", reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("reminder:"))
    def handle_reminder_choice(call) -> None:
        habit_id = int(call.data.split(":")[1])
        telegram_id = call.from_user.id

        with bot.retrieve_data(telegram_id, call.message.chat.id) as data:
            data["reminder_habit_id"] = habit_id

        bot.set_state(
            telegram_id, ReminderStates.waiting_for_time, call.message.chat.id
        )
        bot.edit_message_text(
            "Введите время напоминания в формате ЧЧ:ММ (например, 09:30):",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )

    @bot.message_handler(state=ReminderStates.waiting_for_time)
    def handle_reminder_time(message: Message) -> None:
        telegram_id = message.from_user.id
        raw_time = message.text.strip() if message.text else ""

        try:
            hours, minutes = (int(part) for part in raw_time.split(":"))
            if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                raise ValueError
            reminder_time = f"{hours:02d}:{minutes:02d}:00"
        except ValueError:
            bot.send_message(
                telegram_id,
                "Неверный формат времени. Используйте ЧЧ:ММ, например, 09:30:",
            )
            return

        with bot.retrieve_data(telegram_id, message.chat.id) as data:
            habit_id = data.get("reminder_habit_id")

        bot.delete_state(telegram_id, message.chat.id)

        if not habit_id:
            bot.send_message(
                telegram_id, "Ошибка состояния. Начните заново /set_reminder"
            )
            return

        updated = api_client.update_habit(
            telegram_id, habit_id, {"reminder_time": reminder_time}
        )

        if updated is None:
            bot.send_message(telegram_id, "❌ Не удалось установить напоминание.")
            return

        logger.bind(sent_message=True).info(
            "Установлено напоминание {} для привычки {} пользователя {}",
            reminder_time,
            habit_id,
            telegram_id,
        )
        bot.send_message(telegram_id, f"⏰ Напоминание установлено на {raw_time}!")
