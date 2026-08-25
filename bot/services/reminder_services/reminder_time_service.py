"""
Сервис обработки ввода времени напоминания.

Содержит функцию, которая вызывается на финальном шаге установки
напоминания: валидирует введённое время в формате ``ЧЧ:ММ``,
извлекает из FSM-данных идентификатор привычки, отправляет запрос
на обновление через API-клиент и сбрасывает состояние пользователя.
"""

from loguru import logger
from telebot import TeleBot
from telebot.types import Message

from bot.api.api_client import api_client


def show_reminder_time(bot: TeleBot, message: Message) -> None:
    """
    Обработать ввод времени напоминания и установить его для привычки.

    Разбивает введённый текст по символу ":" и преобразует
    части в часы и минуты. Проверяет, что часы находятся в диапазоне
    0–23, а минуты — 0–59. При невалидном формате или значении
    запрашивает повторный ввод без изменения состояния.

    Извлекает из данных состояния (FSM) идентификатор привычки
    (ключ "reminder_habit_id") и сбрасывает FSM-состояние
    пользователя. Если идентификатор отсутствует — отправляет
    сообщение об ошибке состояния с подсказкой начать заново.

    Формирует полезную нагрузку {"reminder_time": reminder_time}
    (в формате ЧЧ:ММ:СС) и отправляет запрос на обновление
    через api_client.update_habit. Если обновление не удалось
    (возвращён None) — уведомляет пользователя. При успехе
    записывает событие в лог через loguru.logger и отправляет
    подтверждение с установленным временем.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param message: Входящее сообщение со временем в формате ЧЧ:ММ
    :type message: Message
    :return: Ничего не возвращает
    :rtype: None
    """

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

    if habit_id is None:
        bot.send_message(telegram_id, "Ошибка состояния. Начните заново /set_reminder")
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
