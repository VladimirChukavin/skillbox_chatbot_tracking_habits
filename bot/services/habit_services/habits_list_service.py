"""
Сервис отображения списка привычек пользователя.

Содержит функцию, которая запрашивает у backend список всех
привычек пользователя через API-клиент и формирует из них
читаемое текстовое сообщение с прогрессом выполнения.
"""

from telebot import TeleBot

from bot.api.api_client import api_client


def show_habits_list(bot: TeleBot, telegram_id: int, chat_id: int) -> None:
    """
    Показать список всех привычек пользователя.

    Запрашивает список привычек через api_client.list_habits.
    Если привычек нет — отправляет в чат уведомление с подсказкой
    использовать команду /add_habit. Если список непустой —
    формирует текстовое сообщение и пронумерованный перечень,
    где для каждой привычки отображается название и прогресс в
    формате completed_count/target_days, и отправляет его
    пользователю.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param telegram_id: Идентификатор Telegram-пользователя
    :type telegram_id: int
    :param chat_id: Идентификатор чата, куда отправить сообщение
    :type chat_id: int
    :return: Ничего не возвращает
    :rtype: None
    """

    habits = api_client.list_habits(telegram_id)

    if not habits:
        bot.send_message(
            telegram_id, "У вас пока нет привычек. Добавьте через /add_habit"
        )
        return

    text_lines = ["📋 Ваши привычки:\n"]

    for index, habit in enumerate(habits, start=1):
        text_lines.append(
            f"{index}. {habit['title']} - прогресс {habit['completed_count']}/"
            f"{habit['target_days']}"
        )

    bot.send_message(telegram_id, "\n".join(text_lines))
