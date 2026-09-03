"""
Универсальный сервис отмены текущего действия пользователя.

Содержит функцию, которая обрабатывает отмену любого текущего
процесса (создание, редактирование и т.д.) по нажатию кнопки
или текстовой команде, сбрасывает FSM-состояние и уведомляет
пользователя об успешной отмене.
"""

from telebot import TeleBot
from telebot.types import CallbackQuery, Message


def show_cancel(bot: TeleBot, call_or_message: CallbackQuery | Message) -> None:
    """
    Обработать отмену текущего действия пользователя.

    Определяет тип входящего события (CallbackQuery от inline-кнопки
    или Message от текстового сообщения) и извлекает идентификаторы
    пользователя и чата. После этого сбрасывает FSM-состояние пользователя,
    чтобы прервать текущий диалог, и отправляет сообщение об успешной
    отмене.

    Если событие пришло от inline-кнопки, функция также вызывает
    bot.answer_callback_query, чтобы убрать индикатор загрузки (спиннер)
    с нажатой кнопки.

    :param bot: Экземпляр Telegram-бота
    :type bot: TeleBot
    :param call_or_message: Объект запроса от inline-кнопки или входящее сообщение
    :type call_or_message: Union[CallbackQuery, Message]
    :return: Ничего не возвращает
    :rtype: None
    """

    if hasattr(call_or_message, "message"):
        telegram_id = call_or_message.from_user.id
        chat_id = call_or_message.message.chat.id
        bot.answer_callback_query(call_or_message.id)
    else:
        telegram_id = call_or_message.from_user.id
        chat_id = call_or_message.chat.id

    bot.delete_state(telegram_id, chat_id)
    bot.send_message(telegram_id, "Действие отменено.")
