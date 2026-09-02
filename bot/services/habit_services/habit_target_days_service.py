"""
Сервис обработки ввода срока привычки и её создания.

Содержит функцию, которая вызывается на финальном шаге формы
добавления привычки: валидирует введённое количество дней, собирает
все ранее введённые данные из FSM, отправляет запрос на создание
привычки через API-клиент и сбрасывает состояние пользователя.
"""

from loguru import logger
from telebot import TeleBot
from telebot.types import Message

from bot.api.api_client import api_client


def show_habit_target_days(bot: TeleBot, message: Message) -> None:
    """
    Обработать ввод срока привычки и создать привычку.

    Проверяет, что сообщение содержит текст. Преобразует введённое
    значение в целое число и валидирует его: число должно находиться
    в диапазоне от 1 до 365. При невалидном вводе запрашивает
    повторный ввод без изменения состояния.

    Извлекает из данных состояния (FSM) ранее введённые значения
    (title, description, target_description) и добавляет
    к ним target_days. Сбрасывает FSM-состояние пользователя
    и отправляет запрос на создание привычки через
    api_client.create_habit.

    Если создание не удалось (возвращён None) — уведомляет
    пользователя с подсказкой о возможной необходимости авторизации.
    При успехе записывает событие в лог через loguru.logger и
    отправляет подтверждение с названием созданной привычки.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param message: Входящее сообщение со сроком в днях
    :type message: Message
    :return: Ничего не возвращает
    :rtype: None
    """

    telegram_id = message.from_user.id

    if not isinstance(message.text, str):
        bot.send_message(telegram_id, "Пожалуйста, введите число от 1 до 365:")
        return

    raw_days = message.text.strip()

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

    created = None

    try:
        created = api_client.create_habit(telegram_id, habit_data)
    except Exception as error:
        logger.error("Ошибка при создании привычки: {}", error)
        bot.send_message(
            telegram_id, "❌ Произошла ошибка при создании привычки. Попробуйте позже."
        )
        return

    if created is None:
        bot.send_message(
            telegram_id, "❌ Не удалось создать привычку. Проверьте введенные данные."
        )
        return

    bot.delete_state(telegram_id, message.chat.id)

    logger.bind(sent_message=True).info(
        "Создана привычка {} для пользователя {}", created.get("title"), telegram_id
    )
    bot.send_message(telegram_id, f"✅ Привычка \"{created['title']}\" добавлена!")
