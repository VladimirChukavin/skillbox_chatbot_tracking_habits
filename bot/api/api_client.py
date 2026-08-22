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
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.trust_env = False

    def register_user(
        self, telegram_id: int, full_name: str, password: str, username: str | None
    ) -> dict[str, Any] | None:
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
        return login_user_service(
            self._session,
            self._base_url,
            bot_settings,
            telegram_id,
            password,
        )

    def create_habit(self, telegram_id: int, habit_data: dict) -> dict | None:
        return create_habit_service(
            self._session,
            self._base_url,
            "POST",
            telegram_id,
            habit_data,
        )

    def list_habits(self, telegram_id: int) -> list[dict]:
        return list_habits_service(
            self._session,
            self._base_url,
            "GET",
            telegram_id,
            "/habits",
        )

    def get_habit(self, telegram_id: int, habit_id: int) -> dict | None:
        return get_habit_service(
            self._session,
            self._base_url,
            "GET",
            telegram_id,
            habit_id,
        )

    def update_habit(
        self, telegram_id: int, habit_id: int, habit_data: dict
    ) -> dict | None:
        return update_habit_service(
            self._session,
            self._base_url,
            "PATCH",
            telegram_id,
            habit_id,
            habit_data,
        )

    def delete_habit(self, telegram_id: int, habit_id: int) -> bool:
        return delete_habit_service(
            self._session,
            self._base_url,
            "DELETE",
            telegram_id,
            habit_id,
        )

    def track_habit(
        self, telegram_id: int, habit_id: int, is_completed: bool
    ) -> dict | None:
        return track_habit_service(
            self._session,
            self._base_url,
            "POST",
            telegram_id,
            habit_id,
            is_completed,
        )

    def get_habit_stats(self, telegram_id: int, habit_id: int) -> dict | None:
        return get_habit_stats_service(
            self._session,
            self._base_url,
            "GET",
            telegram_id,
            habit_id,
        )


api_client = ApiClient(bot_settings.api_base_url)
