from bot.storage import TokenBundle, token_storage


def _store_tokens(telegram_id: int, token_data: dict) -> None:
    token_storage.save_tokens(
        telegram_id,
        TokenBundle(
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
        ),
    )
