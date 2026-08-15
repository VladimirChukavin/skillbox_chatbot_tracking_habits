from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    telegram_token: str
    api_base_url: str
    request_timeout: int = 15
    debug: bool = False
    http_proxy: str | None = None
    https_proxy: str | None = None


bot_settings = BotSettings()
