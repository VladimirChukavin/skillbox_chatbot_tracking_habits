import threading
from dataclasses import dataclass


@dataclass
class TokenBundle:
    access_token: str
    refresh_token: str


class TokenStorage:
    def __init__(self) -> None:
        self._tokens: dict[int, TokenBundle] = {}
        self._lock = threading.Lock()

    def save_tokens(self, telegram_id: int, bundle: TokenBundle) -> None:
        with self._lock:
            self._tokens[telegram_id] = bundle

    def get_tokens(self, telegram_id: int) -> TokenBundle | None:
        with self._lock:
            return self._tokens.get(telegram_id)

    def clear_tokens(self, telegram_id: int) -> None:
        with self._lock:
            self._tokens.pop(telegram_id, None)


token_storage = TokenStorage()
