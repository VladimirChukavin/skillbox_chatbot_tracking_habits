"""
Общие фикстуры для тестов бота.
"""

import os

os.environ.setdefault("TELEGRAM_TOKEN", "test-token")
os.environ.setdefault("API_BASE_URL", "https://localhost:8000")
os.environ.setdefault("REQUEST_TIMEOUT", "15")
os.environ.setdefault("DEBUG", "false")

from unittest.mock import MagicMock  # noqa: E402

import pytest  # noqa: E402

from bot.storage import TokenBundle, token_storage  # noqa: E402


@pytest.fixture(autouse=True)
def refresh_token_storage():
    token_storage._tokens.clear()
    yield
    token_storage._tokens.clear()


@pytest.fixture
def token_bundle():
    return TokenBundle(access_token="access123", refresh_token="refresh456")


@pytest.fixture
def mock_response():
    def _create(status_code=200, json_data=None):
        resp = MagicMock()
        resp.status_code = status_code
        resp.json.return_value = json_data or {}
        resp.text = ""
        return resp

    return _create
