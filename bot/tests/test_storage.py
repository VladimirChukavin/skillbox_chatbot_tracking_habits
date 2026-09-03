"""
Тесты функций для работы с хранилищем токенов
"""

from unittest.mock import MagicMock

from bot.storage import TokenBundle, TokenStorage, token_storage


class TestTokenBundle:
    def test_creation(self):
        bundle = TokenBundle(access_token="a", refresh_token="r")
        assert bundle.access_token == "a"
        assert bundle.refresh_token == "r"


class TestTokenStorage:
    def test_save_and_get_tokens(self):
        storage = MagicMock(spec=TokenStorage)
        bundle = TokenBundle(access_token="a", refresh_token="r")

        storage.save_tokens = MagicMock()
        storage.get_tokens = MagicMock(return_value=bundle)

        storage.save_tokens(123, bundle)
        result = storage.get_tokens(123)

        assert result is bundle

    def test_get_tokens_not_found(self):
        storage = MagicMock(spec=TokenStorage)
        storage.get_tokens = MagicMock(return_value=None)
        assert storage.get_tokens(999) is None

    def test_clear_tokens(self):
        storage = MagicMock(spec=TokenStorage)
        storage.clear_tokens = MagicMock()
        storage.get_tokens = MagicMock(return_value=None)

        storage.clear_tokens(123)
        storage.clear_tokens.assert_called_once_with(123)
        assert storage.get_tokens(123) is None

    def test_clear_tokens_nonexistent_no_error(self):
        storage = MagicMock(spec=TokenStorage)
        storage.clear_tokens = MagicMock()
        storage.clear_tokens(999)
        storage.clear_tokens.assert_called_once_with(999)

    def test_overwrite_tokens(self):
        storage = MagicMock(spec=TokenStorage)
        bundle1 = TokenBundle(access_token="a1", refresh_token="r1")
        bundle2 = TokenBundle(access_token="a2", refresh_token="r2")

        storage.get_tokens = MagicMock(side_effect=[bundle1, bundle2])
        storage.save_tokens = MagicMock()

        storage.save_tokens(123, bundle1)
        assert storage.get_tokens(123) is bundle1

        storage.save_tokens(123, bundle2)
        assert storage.get_tokens(123) is bundle2

    def test_global_instance_is_token_storage(self):
        assert isinstance(token_storage, TokenStorage)
