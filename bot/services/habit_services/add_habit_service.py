"""
Сервис добавления новой привычки.

Содержит функцию, которая инициирует процесс создания привычки:
проверяет авторизацию пользователя и переводит его в состояние
ожидания ввода названия (первый шаг формы).
"""

from loguru import logger
from telebot import TeleBot

from bot.states import AddHabitStates
from bot.storage import token_storage


def show_add_habit(bot: TeleBot, telegram_id: int, chat_id: int) -> None:
    """
    Инициировать процесс добавления новой привычки.

    Проверяет наличие сохранённых токенов авторизации для текущего
    Telegram-пользователя. Если токены отсутствуют — действие
    прерывается без уведомления. Если токены есть — переводит
    пользователя в состояние ожидания ввода названия привычки
    (AddHabitStates.waiting_for_title) и отправляет
    соответствующее сообщение в чат.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param telegram_id: Идентификатор Telegram-пользователя
    :type telegram_id: int
    :param chat_id: Идентификатор чата, куда отправить сообщение
    :type chat_id: int
    :return: Ничего не возвращает
    :rtype: None
    """

    if token_storage.get_tokens(telegram_id) is None:
        bot.send_message(
            chat_id, "❌ Вы не авторизованы. Введите /login для доступа к боту."
        )
        logger.warning(
            "Попытка добавить привычку без авторизации (telegram_id={})", telegram_id
        )
        return

    bot.set_state(telegram_id, AddHabitStates.waiting_for_title, chat_id)
    bot.send_message(chat_id, "Введите название привычки:")
