"""
Тесты API-сервисов бота (с моками requests).
"""

from unittest.mock import MagicMock, patch

import pytest

from bot.api.api_services.authorized_request_service import _authorized_request
from bot.api.api_services.create_habit_service import create_habit_service
from bot.api.api_services.delete_habit_service import delete_habit_service
from bot.api.api_services.get_habit_stats_service import get_habit_stats_service
from bot.api.api_services.list_habits_service import list_habits_service
from bot.api.api_services.login_user_service import login_user_service
from bot.api.api_services.refresh_access_token_service import _refresh_access_token
from bot.api.api_services.register_user_service import register_user_service
from bot.api.api_services.store_tokens_service import _store_tokens
from bot.api.api_services.track_habit_service import track_habit_service
from bot.storage import TokenBundle, token_storage


class TestStoreTokens:
    def test_store_tokens_saves_to_storage(self):
        _store_tokens(123, {"access_token": "a", "refresh_token": "r"})

        bundle = token_storage.get_tokens(123)
        assert bundle is not None
        assert bundle.access_token == "a"
        assert bundle.refresh_token == "r"


class TestRegisterUserService:
    def test_register_success(self, mock_response):
        session = MagicMock()
        session.post.return_value = mock_response(
            status_code=201,
            json_data={"access_token": "a", "refresh_token": "r"},
        )
        settings = MagicMock()
        settings.request_timeout = 15

        result = register_user_service(
            session,
            "http://localhost:8000",
            settings,
            telegram_id=123,
            full_name="Иван",
            password="secret123",
            username="ivan",
        )

        assert result is not None
        assert result["access_token"] == "a"
        assert token_storage.get_tokens(123) is not None

    def test_register_failure_returns_none(self, mock_response):
        session = MagicMock()
        session.post.return_value = mock_response(
            status_code=400, json_data={"detail": "error"}
        )
        settings = MagicMock()
        settings.request_timeout = 15

        result = register_user_service(
            session,
            "http://localhost:8000",
            settings,
            telegram_id=123,
            full_name="Иван",
            password="secret123",
            username="ivan",
        )

        assert result is None


class TestLoginUserService:
    def test_login_success(self, mock_response):
        session = MagicMock()
        session.post.return_value = mock_response(
            status_code=200,
            json_data={"access_token": "a", "refresh_token": "r"},
        )
        settings = MagicMock()
        settings.request_timeout = 15

        result = login_user_service(
            session,
            "http://localhost:8000",
            settings,
            telegram_id=123,
            password="secret123",
        )

        assert result is not None
        assert token_storage.get_tokens(123) is not None

    def test_login_failure_returns_none(self, mock_response):
        session = MagicMock()
        session.post.return_value = mock_response(status_code=401)
        settings = MagicMock()
        settings.request_timeout = 15

        result = login_user_service(
            session,
            "http://localhost:8000",
            settings,
            telegram_id=123,
            password="secret123",
        )

        assert result is None


class TestRefreshAccessToken:
    def test_refresh_success(self, mock_response, token_bundle):
        token_storage.save_tokens(123, token_bundle)
        session = MagicMock()
        session.post.return_value = mock_response(
            status_code=200,
            json_data={"access_token": "new_a", "refresh_token": "new_r"},
        )

        result = _refresh_access_token(123, session, "http://localhost:8000")

        assert result is True
        bundle = token_storage.get_tokens(123)
        assert bundle.access_token == "new_a"

    def test_refresh_no_tokens(self):
        session = MagicMock()
        result = _refresh_access_token(999, session, "http://localhost:8000")

        assert result is False

    def test_refresh_failure_clears_tokens(self, mock_response, token_bundle):
        token_storage.save_tokens(123, token_bundle)
        session = MagicMock()
        session.post.return_value = mock_response(status_code=401)

        result = _refresh_access_token(123, session, "http://localhost:8000")

        assert result is False
        assert token_storage.get_tokens(123) is None


class TestAuthorizedRequest:
    def test_no_tokens_returns_none(self):
        session = MagicMock()
        result = _authorized_request(
            session, "http://localhost:8000", "GET", 999, "/habits"
        )

        assert result is None

    def test_successful_request(self, mock_response, token_bundle):
        token_storage.save_tokens(123, token_bundle)
        session = MagicMock()
        session.request.return_value = mock_response(status_code=200, json_data=[])

        result = _authorized_request(
            session, "http://localhost:8000", "GET", 123, "/habits"
        )

        assert result is not None
        assert result.status_code == 200

    def test_unathorized_triggers_refresh(self, mock_response, token_bundle):
        token_storage.save_tokens(123, token_bundle)
        session = MagicMock()
        session.request.side_effect = [
            mock_response(status_code=401),
            mock_response(status_code=200, json_data=[]),
        ]
        session.post.return_value = mock_response(
            status_code=200,
            json_data={"access_token": "new_r", "refresh_token": "new_r"},
        )

        result = _authorized_request(
            session, "http://localhost:8000", "GET", 123, "/habits"
        )

        assert result is not None
        assert result.status_code == 200
        assert session.request.call_count == 2


class TestCreateHabitsService:
    def test_create_habit_success(self, mock_response, token_bundle):
        token_storage.save_tokens(123, token_bundle)
        session = MagicMock()
        session.request.return_value = mock_response(
            status_code=201, json_data={"id": 1, "title": "Test"}
        )

        result = create_habit_service(
            session,
            "http://localhost:8000",
            123,
            {"title": "Test", "target_days": 21},
        )

        assert result is not None
        assert result["id"] == 1

    def test_create_habit_failure(self, mock_response, token_bundle):
        token_storage.save_tokens(123, token_bundle)
        session = MagicMock()
        session.request.return_value = mock_response(status_code=400)

        result = create_habit_service(
            session,
            "http://localhost:8000",
            123,
            {"title": "Test"},
        )

        assert result is None

    def test_create_habit_no_tokens(self):
        session = MagicMock()
        result = create_habit_service(
            session,
            "http://localhost:8000",
            999,
            {"title": "Test"},
        )

        assert result is None


class TestListHabitsService:
    def test_list_success(self, mock_response, token_bundle):
        token_storage.save_tokens(123, token_bundle)
        session = MagicMock()
        session.request.return_value = mock_response(
            status_code=200,
            json_data=[{"id": 1, "title": "Test"}],
        )

        result = list_habits_service(session, "http://localhost:8000", 123, "/habits")

        assert len(result) == 1
        assert result[0]["title"] == "Test"

    def test_list_no_tokens_returns_empty(self):
        session = MagicMock()
        result = list_habits_service(session, "http://localhost:8000", 999, "/habits")

        assert result == []

    def test_list_error_returns_empty(self, mock_response, token_bundle):
        token_storage.save_tokens(123, token_bundle)
        session = MagicMock()
        session.request.return_value = mock_response(status_code=500)

        result = list_habits_service(session, "http://localhost:8000", 123, "/habits")

        assert result == []


class TestDeleteHabitService:
    def test_delete_success(self, mock_response, token_bundle):
        token_storage.save_tokens(123, token_bundle)
        session = MagicMock()
        session.request.return_value = mock_response(status_code=204)

        result = delete_habit_service(session, "http://localhost:8000", 123, 1)

        assert result is True

    def test_delete_failure(self, mock_response, token_bundle):
        token_storage.save_tokens(123, token_bundle)
        session = MagicMock()
        session.request.return_value = mock_response(status_code=404)

        result = delete_habit_service(session, "http://localhost:8000", 123, 99)

        assert result is False

    def test_delete_no_tokens(self):
        session = MagicMock()

        result = delete_habit_service(session, "http://localhost:8000", 999, 1)

        assert result is False


class TestTrackHabitsService:
    def test_track_success(self, mock_response, token_bundle):
        token_storage.save_tokens(123, token_bundle)
        session = MagicMock()
        session.request.return_value = mock_response(
            status_code=200,
            json_data={"id": 1, "completed_count": 1},
        )

        result = track_habit_service(session, "http://localhost:8000", 123, 1, True)

        assert result is not None
        assert result["completed_count"] == 1

    def test_track_failure(self, mock_response, token_bundle):
        token_storage.save_tokens(123, token_bundle)
        session = MagicMock()
        session.request.return_value = mock_response(status_code=400)

        result = track_habit_service(session, "http://localhost:8000", 123, 1, True)

        assert result is None


class TestGetHabitsStatsService:
    def test_stats_success(self, mock_response, token_bundle):
        token_storage.save_tokens(123, token_bundle)
        session = MagicMock()
        session.request.return_value = mock_response(
            status_code=200,
            json_data={"habit_id": 1, "progress_percent": 50.0},
        )

        result = get_habit_stats_service(session, "http://localhost:8000", 123, 1)

        assert result is not None
        assert result["progress_percent"] == 50.0

    def test_stats_failure(self, mock_response, token_bundle):
        token_storage.save_tokens(123, token_bundle)
        session = MagicMock()
        session.request.return_value = mock_response(status_code=404)

        result = get_habit_stats_service(session, "http://localhost:8000", 123, 99)

        assert result is None
