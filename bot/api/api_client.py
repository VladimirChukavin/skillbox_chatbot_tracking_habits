"""
Клиент для взаимодействия с REST API бэкенда.

Предоставляет класс ApiClient, который инкапсулирует HTTP-запросы
к бэкенду, управляет сессией requests и делегирует выполнение
конкретным сервисам из bot.api.api_services.
"""

from typing import Any

import requests

from bot.api.api_services.create_habit_service import create_habit_service
from bot.api.api_services.delete_habit_service import delete_habit_service
from bot.api.api_services.get_habit_service import get_habit_service
from bot.api.api_services.get_habit_stats_service import get_habit_stats_service
from bot.api.api_services.list_habits_service import list_habits_service
from bot.api.api_services.login_user_service import login_user_service
from bot.api.api_services.register_user_service import register_user_service
from bot.api.api_services.track_habit_service import track_habit_service
from bot.api.api_services.update_habit_service import update_habit_service
from bot.config import bot_settings


class ApiClient:
    """
    Клиент для выполнения запросов к API бэкенда.

    Управляет переиспользуемой HTTP-сессией и обеспечивает единый интерфейс
    для всех операций (аутентификация, CRUD привычек, трекинг, статистика).

    :param base_url: Базовый URL API бэкенда
    :type base_url: str
    """

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.trust_env = False

    def register_user(
        self, telegram_id: int, full_name: str, password: str, username: str | None
    ) -> dict[str, Any] | None:
        """
        Зарегистрировать нового пользователя на бэкенде.

        :param telegram_id: Telegram ID пользователя
        :type telegram_id: int
        :param full_name: Полное имя пользователя
        :type full_name: str
        :param password: Пароль пользователя
        :type password: str
        :param username: Username пользователя в Telegram
        :type username: str | None
        :return: Словарь с токенами при успехе, иначе None
        :rtype: dict[str, Any] | None
        """

        return register_user_service(
            self._session,
            self._base_url,
            bot_settings,
            telegram_id,
            full_name,
            password,
            username,
        )

    def login_user(self, telegram_id: int, password: str) -> dict[str, Any] | None:
        """
        Выполнить вход пользователя на бэкенде.

        :param telegram_id: Telegram ID пользователя
        :type telegram_id: int
        :param password: Пароль пользователя
        :type password: str
        :return: Словарь с токенами при успехе, иначе None
        :rtype: dict[str, Any] | None
        """

        return login_user_service(
            self._session,
            self._base_url,
            bot_settings,
            telegram_id,
            password,
        )

    def create_habit(self, telegram_id: int, habit_data: dict) -> dict | None:
        """
        Создать новую привычку для пользователя.

        :param telegram_id: Telegram ID пользователя
        :type telegram_id: int
        :param habit_data: Данные для создания привычки
        :type habit_data: dict
        :return: Словарь с данными созданной привычки или None
        :rtype: dict | None
        """

        return create_habit_service(
            self._session,
            self._base_url,
            telegram_id,
            habit_data,
        )

    def list_habits(self, telegram_id: int) -> list[dict]:
        """
        Получить список всех привычек пользователя.

        :param telegram_id: Telegram ID пользователя
        :type telegram_id: int
        :return: Список словарей с привычками (пустой список при ошибке)
        :rtype: list[dict]
        """

        return list_habits_service(
            self._session,
            self._base_url,
            telegram_id,
            "/habits",
        )

    def get_habit(self, telegram_id: int, habit_id: int) -> dict | None:
        """
        Получить данные конкретной привычки.

        :param telegram_id: Telegram ID пользователя
        :type telegram_id: int
        :param habit_id: Идентификатор привычки
        :type habit_id: int
        :return: Словарь с данными привычки или None
        :rtype: dict | None
        """

        return get_habit_service(
            self._session,
            self._base_url,
            telegram_id,
            habit_id,
        )

    def update_habit(
        self, telegram_id: int, habit_id: int, habit_data: dict
    ) -> dict | None:
        """
        Обновить данные привычки.

        :param telegram_id: Telegram ID пользователя
        :type telegram_id: int
        :param habit_id: Идентификатор привычки
        :type habit_id: int
        :param habit_data: Данные для обновления
        :type habit_data: dict
        :return: Словарь с обновлёнными данными или None
        :rtype: dict | None
        """

        return update_habit_service(
            self._session,
            self._base_url,
            telegram_id,
            habit_id,
            habit_data,
        )

    def delete_habit(self, telegram_id: int, habit_id: int) -> bool:
        """
        Удалить привычку.

        :param telegram_id: Telegram ID пользователя
        :type telegram_id: int
        :param habit_id: Идентификатор удаляемой привычки
        :type habit_id: int
        :return: True при успешном удалении, иначе False
        :rtype: bool
        """

        return delete_habit_service(
            self._session,
            self._base_url,
            telegram_id,
            habit_id,
        )

    def track_habit(
        self, telegram_id: int, habit_id: int, is_completed: bool
    ) -> dict | None:
        """
        Отметить выполнение привычки за текущий день.

        :param telegram_id: Telegram ID пользователя
        :type telegram_id: int
        :param habit_id: Идентификатор привычки
        :type habit_id: int
        :param is_completed: Статус выполнения (True/False)
        :type is_completed: bool
        :return: Словарь с обновлённой привычкой или None
        :rtype: dict | None
        """

        return track_habit_service(
            self._session,
            self._base_url,
            telegram_id,
            habit_id,
            is_completed,
        )

    def get_habit_stats(self, telegram_id: int, habit_id: int) -> dict | None:
        """
        Получить статистику выполнения привычки.

        :param telegram_id: Telegram ID пользователя
        :type telegram_id: int
        :param habit_id: Идентификатор привычки
        :type habit_id: int
        :return: Словарь со статистикой или None
        :rtype: dict | None
        """

        return get_habit_stats_service(
            self._session,
            self._base_url,
            telegram_id,
            habit_id,
        )


api_client = ApiClient(bot_settings.api_base_url)
