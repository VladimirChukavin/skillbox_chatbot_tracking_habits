from telebot import TeleBot
from telebot.types import Message
from loguru import logger

from bot.api_client import api_client
from bot.keyboards import build_edit_fields_keyboard, build_habits_keyboard
from bot.states import AddHabitStates, EditHabitStates


def register_habit_handlers(bot: TeleBot) -> None:
    @bot.message_handler(commands=["add_habit"])
    def handle_add_habit(message: Message) -> None:
        telegram_id = message.from_user.id
        bot.set_state(telegram_id, AddHabitStates.waiting_for_title, message.chat.id)
        bot.send_message(telegram_id, "Введите название привычки:")

    @bot.message_handler(state=AddHabitStates.waiting_for_title)
    def handle_habit_title(message: Message) -> None:
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

    @bot.message_handler(state=AddHabitStates.waiting_for_description)
    def handle_habit_description(message: Message) -> None:
        description = message.text.strip() if message.text else ""

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

    @bot.message_handler(state=AddHabitStates.waiting_for_target_description)
    def handle_habit_target(message: Message) -> None:
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

    @bot.message_handler(state=AddHabitStates.waiting_for_target_days)
    def handle_habit_target_days(message: Message) -> None:
        telegram_id = message.from_user.id
        raw_days = message.text.strip() if message.text else "21"

        try:
            target_days = int(raw_days)
            if target_days < 1 or target_days > 365:
                raise ValueError
        except ValueError:
            bot.send_message(telegram_id, "Введите число от 1 до 365:")
            return

        with bot.retrieve_data(telegram_id, message.chat.id) as data:
            habit_data = {
                "title": data.get("title"),
                "description": data.get("description"),
                "target_description": data.get("target_description"),
                "target_days": target_days,
            }

        bot.delete_state(telegram_id, message.chat.id)

        created = api_client.create_habit(telegram_id, habit_data)

        if created is None:
            bot.send_message(
                telegram_id, "❌ Не удалось создать привычку. Вы авторизованы? /login"
            )
            return

        logger.bind(sent_message=True).info(
            "Создана привычка {} для пользователя {}", created.get("title"), telegram_id
        )
        bot.send_message(telegram_id, f"✅ Привычка \"{created['title']}\" добавлена!")

    @bot.message_handler(commands=["habits"])
    def handle_list_habits(message: Message) -> None:
        telegram_id = message.from_user.id
        habits = api_client.list_habits(telegram_id)

        if not habits:
            bot.send_message(
                telegram_id, "У вас пока нет привычек. Добавьте через /add_habit"
            )
            return

        text_lines = ["📋 Ваши привычки:\n"]

        for index, habit in enumerate(habits, start=1):
            text_lines.append(
                f"{index}. *{habit['title']}* - прогресс {habit['completed_count']}/"
                f"{habit['target_days']}"
            )

        bot.send_message(telegram_id, "\n".join(text_lines), parse_mode="Markdown")

    @bot.message_handler(commands=["edit_habit"])
    def handle_edit_habit(message: Message) -> None:
        telegram_id = message.from_user.id
        habits = api_client.list_habits(telegram_id)

        if not habits:
            bot.send_message(telegram_id, "❌ Нет привычек для редактирования.")
            return

        bot.set_state(
            telegram_id,
            EditHabitStates.waiting_for_habit_choice,
            message.chat.id,
        )
        keyboard = build_habits_keyboard(habits, callback_prefix="edit")
        bot.send_message(
            telegram_id,
            "Выберите привычку:",
            reply_markup=keyboard,
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("edit:"))
    def handle_edit_habit_choice(call) -> None:
        habit_id = int(call.data.split(":")[1])
        telegram_id = call.from_user.id

        with bot.retrieve_data(telegram_id, call.message.chat.id) as data:
            data["editing_habit_id"] = habit_id

        bot.set_state(
            telegram_id,
            EditHabitStates.waiting_for_field_choice,
            call.message.chat.id,
        )
        bot.edit_message_text(
            "Что вы хотите изменить?",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=build_edit_fields_keyboard(),
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("field:"))
    def handle_field_choice(call) -> None:
        field = call.data.split(":")[1]
        telegram_id = call.from_user.id

        if field == "delete":
            with bot.retrieve_data(telegram_id, call.message.chat.id) as data:
                habit_id = data.get("editing_habit_id")

            if habit_id and api_client.delete_habit(telegram_id, habit_id):
                bot.delete_state(telegram_id, call.message.chat.id)
                bot.edit_message_text(
                    "🗑 Привычка удалена.",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                )
            else:
                bot.send_message(telegram_id, "❌ Не удалось удалить привычку.")
            return

        with bot.retrieve_data(telegram_id, call.message.chat.id) as data:
            data["editing_field"] = field

        bot.set_state(
            telegram_id,
            EditHabitStates.waiting_for_new_value,
            call.message.chat.id,
        )
        field_labels = {
            "title": "новое название",
            "description": "новое описание",
            "target_description": "новая цель",
            "target_days": "новый срок в днях",
        }
        bot.edit_message_text(
            f"Введите {field_labels.get(field, 'новое значение')}:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )

    @bot.message_handler(state=EditHabitStates.waiting_for_new_value)
    def handle_new_value(message: Message) -> None:
        telegram_id = message.from_user.id

        with bot.retrieve_data(telegram_id, message.chat.id) as data:
            habit_id = data.get("editing_habit_id")
            field = data.get("editing_field")

        if not habit_id or not field:
            bot.send_message(
                telegram_id, "Ошибка состояния. Начните заново /edit_habit"
            )
            bot.delete_state(telegram_id, message.chat.id)
            return

        value: str | int = message.text.strip() if message.text else ""

        if field == "target_days":
            try:
                value = int(value)
            except ValueError:
                bot.send_message(telegram_id, "Введите число:")
                return

        update_payload = {field: value}
        updated = api_client.update_habit(telegram_id, habit_id, update_payload)
        bot.delete_state(telegram_id, message.chat.id)

        if updated is None:
            bot.send_message(telegram_id, "❌ Не удалось обновить привычку.")
            return

        logger.bind(sent_message=True).info(
            "Привычка {} обновлена пользователем {}", habit_id, telegram_id
        )
        bot.send_message(telegram_id, "✅ Привычка обновлена!")
