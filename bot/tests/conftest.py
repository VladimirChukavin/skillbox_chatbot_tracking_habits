"""
Общие фикстуры для тестов бота.
"""

import os

os.environ.setdefault("TELEGRAM_TOKEN", "test-token")
os.environ.setdefault("API_BASE_URL", "https://localhost:8000")
os.environ.setdefault("REQUEST_TIMEOUT", "15")
os.environ.setdefault("DEBUG", "false")
os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PASSWORD", "")
os.environ.setdefault("REDIS_PORT", "6379")
os.environ.setdefault("REDIS_DB", "0")

from unittest.mock import MagicMock  # noqa: E402

import pytest  # noqa: E402

from bot.storage import TokenBundle, token_storage  # noqa: E402


@pytest.fixture(autouse=True)
def create_mock_client():
    mock_data = {}

    def mock_get(key):
        return mock_data.get(key)

    def mock_setex(key, ttl, value):
        mock_data[key] = value

    def mock_delete(key):
        mock_data.pop(key, None)

    mock_client = MagicMock()
    mock_client.get.side_effect = mock_get
    mock_client.setex.side_effect = mock_setex
    mock_client.delete.side_effect = mock_delete

    original_client = token_storage._client
    token_storage._client = mock_client

    yield mock_client

    token_storage._client = original_client


@pytest.fixture
def token_bundle():
    return TokenBundle(access_token="access123", refresh_token="refresh456")


@pytest.fixture
def mock_response():
    def _create(status_code=200, json_data=None):
        resp = MagicMock()
        resp.status_code = status_code
        resp.ok = 200 <= status_code < 400
        resp.json.return_value = json_data or {}
        resp.text = ""
        return resp

    return _create
