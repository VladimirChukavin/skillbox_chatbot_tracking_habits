from typing import Any

import requests
from loguru import logger

from .config import bot_settings
from .storage import TokenBundle, token_storage


class ApiClient:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()

    def register_user(
        self, telegram_id: int, full_name: str, password: str, username: str | None
    ) -> dict[str, Any] | None:
        response = self._session.post(
            f"{self._base_url}/auth/register",
            json={
                "telegram_id": telegram_id,
                "full_name": full_name,
                "password": password,
                "username": username,
            },
            timeout=bot_settings.request_timeout,
        )

        if response.status_code == 201:
            self._store_tokens(telegram_id, response.json())
            return response.json()

        logger.warning(
            "Регистрация не удалась: {} {}", response.status_code, response.text
        )

        return None

    def login_user(self, telegram_id: int, password: str) -> dict[str, Any] | None:
        response = self._session.post(
            f"{self._base_url}/auth/login",
            json={
                "telegram_id": telegram_id,
                "password": password,
            },
            timeout=bot_settings.request_timeout,
        )

        if response.status_code == 200:
            self._store_tokens(telegram_id, response.json())
            return response.json()

        logger.warning("Логин не удался: {} {}", response.status_code, response.text)

        return None

    def _store_tokens(self, telegram_id: int, token_data: dict) -> None:
        token_storage.save_tokens(
            telegram_id,
            TokenBundle(
                access_token=token_data["access_token"],
                refresh_token=token_data["refresh_token"],
            ),
        )

    def _refresh_access_token(self, telegram_id: int) -> bool:
        bundle = token_storage.get_tokens(telegram_id)

        if bundle is None:
            return False

        response = self._session.post(
            f"{self._base_url}/auth/refresh",
            params={"refresh_token": bundle.refresh_token},
            timeout=bot_settings.request_timeout,
        )

        if response.status_code == 200:
            self._store_tokens(telegram_id, response.json())
            return True

        token_storage.clear_tokens(telegram_id)

        return False

    def _authorized_request(
        self, method: str, telegram_id: int, endpoint: str, **kwargs: Any
    ) -> requests.Response | None:
        bundle = token_storage.get_tokens(telegram_id)

        if bundle is None:
            logger.warning("Нет сохраненных токенов для telegram_id={}", telegram_id)
            return None

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {bundle.access_token}"

        response = self._session.request(
            method,
            f"{self._base_url}{endpoint}",
            headers=headers,
            timeout=bot_settings.request_timeout,
            **kwargs,
        )

        if response.status_code == 401:
            if self._refresh_access_token(telegram_id):
                bundle = token_storage.get_tokens(telegram_id)
                headers["Authorization"] = f"Bearer {bundle.access_token}"
                response = self._session.request(
                    method,
                    f"{self._base_url}{endpoint}",
                    headers=headers,
                    timeout=bot_settings.request_timeout,
                    **kwargs,
                )

        return response

    def create_habit(self, telegram_id: int, habit_data: dict) -> dict | None:
        response = self._authorized_request(
            "POST", telegram_id, "/habits/", json=habit_data
        )

        return response.json() if response and response.status_code == 201 else None

    def list_habits(self, telegram_id: int) -> list[dict]:
        response = self._authorized_request("GET", telegram_id, "/habits/")

        if response.status_code == 200:
            return response.json()

        return []

    def get_habit(self, telegram_id: int, habit_id: int) -> dict | None:
        response = self._authorized_request("GET", telegram_id, f"/habits/{habit_id}/")

        return response.json() if response and response.status_code == 200 else None

    def update_habit(
        self, telegram_id: int, habit_id: int, habit_data: dict
    ) -> dict | None:
        response = self._authorized_request(
            "PATCH", telegram_id, f"/habits/{habit_id}", json=habit_data
        )

        return response.json() if response and response.status_code == 200 else None

    def delete_habit(self, telegram_id: int, habit_id: int) -> bool:
        response = self._authorized_request(
            "DELETE", telegram_id, f"/habits/{habit_id}/"
        )

        return response is not None and response.status_code == 204

    def track_habit(
        self, telegram_id: int, habit_id: int, is_completed: bool
    ) -> dict | None:
        response = self._authorized_request(
            "POST",
            telegram_id,
            f"/habits/{habit_id}/track",
            json={"is_completed": is_completed},
        )

        return response.json() if response and response.status_code == 200 else None

    def get_habit_stats(self, telegram_id: int, habit_id: int) -> dict | None:
        response = self._authorized_request(
            "GET", telegram_id, f"/habits/{habit_id}/stats/"
        )

        return response.json() if response and response.status_code == 200 else None


api_client = ApiClient(bot_settings.api_base_url)
