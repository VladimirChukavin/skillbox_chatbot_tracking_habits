"""
Сервис обработки нового значения поля привычки при редактировании.

Содержит функцию, которая вызывается на финальном шаге редактирования:
извлекает из FSM-данных идентификатор привычки и название поля,
валидирует введённое значение, отправляет запрос на обновление
через API-клиент и сбрасывает состояние пользователя.
"""

from loguru import logger
from telebot import TeleBot
from telebot.types import Message

from bot.api.api_client import api_client


def show_habit_new_value(bot: TeleBot, message: Message) -> None:
    """
    Обработать ввод нового значения поля привычки.

    Извлекает из данных состояния (FSM) идентификатор редактируемой
    привычки ("editing_habit_id") и название поля
    ("editing_field"). Если хотя бы один из ключей отсутствует —
    отправляет сообщение об ошибке и сбрасывает состояние.

    Проверяет, что сообщение содержит непустой текст. Если выбранное
    поле — "target_days", пытается преобразовать значение в
    int; при неудаче запрашивает ввод числа.

    Формирует словарь полезной нагрузки вида {field: value} и
    отправляет запрос на обновление через api_client.update_habit.
    После запроса сбрасывает FSM-состояние пользователя. Если
    обновление не удалось (возвращён None) — уведомляет
    пользователя. При успехе записывает событие в лог через
    loguru.logger и отправляет подтверждение.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param message: Входящее сообщение с новым значением поля
    :type message: Message
    :return: Ничего не возвращает
    :rtype: None
    """

    telegram_id = message.from_user.id

    with bot.retrieve_data(telegram_id, message.chat.id) as data:
        habit_id = data.get("editing_habit_id")
        field = data.get("editing_field")

    if habit_id is None or field is None:
        bot.send_message(telegram_id, "Ошибка состояния. Начните заново /edit_habit")
        bot.delete_state(telegram_id, message.chat.id)
        return

    if not message.text:
        bot.send_message(telegram_id, "Пожалуйста, введите текстовое значение:")
        return

    value: str | int = message.text.strip()

    if not value:
        bot.send_message(telegram_id, "Значение не может быть пустым:")
        return

    if field == "target_days":
        try:
            value = int(value)
        except ValueError:
            bot.send_message(telegram_id, "Введите число:")
            return

    update_payload = {field: value}
    updated = None

    try:
        updated = api_client.update_habit(telegram_id, habit_id, update_payload)
    except Exception as error:
        logger.error("Ошибка при обновлении привычки: {}", error)
        bot.send_message(
            telegram_id,
            "❌ Произошла ошибка при обновлении привычки. Попробуйте позже.",
        )

    if updated is None:
        bot.send_message(telegram_id, "❌ Не удалось обновить привычку.")
        return

    bot.delete_state(telegram_id, message.chat.id)

    logger.bind(sent_message=True).info(
        "Привычка {} обновлена пользователем {}", habit_id, telegram_id
    )
    bot.send_message(telegram_id, "✅ Привычка обновлена!")
