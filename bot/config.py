from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("login", "Введите пароль для получения токена на новую сессию"),
    ("add_habit", "Введите название привычки"),
    ("habits", "Ваши привычки"),
    ("edit_habit", "Редактировать привычку"),
    ("set_reminder", "Установить напоминание"),
    ("habit_stats", "Статистика привычек"),
    ("track_habit", "Выберите привычку для трекинга"),
    ("delete_habit", "Удалить привычку"),
)


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    telegram_token: str
    api_base_url: str
    request_timeout: int = 15
    debug: bool = False
    http_proxy: str | None = None
    https_proxy: str | None = None


bot_settings = BotSettings()
