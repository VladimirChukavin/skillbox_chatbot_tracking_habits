"""
Конфигурация бота на базе pydantic-settings.

Содержит кортеж команд бота по умолчанию, класс настроек
BotSettings, загружающий параметры из переменных окружения
(файл .env), и глобальный экземпляр настроек bot_settings,
используемый для всего проекта.
"""

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
    """
    Настройки бота, загружаемые из переменных окружения.

    Чтение переменных производится из файла .env.
    Обязательные параметры (telegram_token, api_base_url)
    должны быть заданы в окружении; остальные имеют значения
    по умолчанию.

    :param telegram_token: Токен Telegram-бота
    :param api_base_url: Базовый URL backend API
    :param request_timeout: Таймаут HTTP-запросов к backend в секундах
    :param debug: Флаг включения отладочного режима (влияет на уровень логирования)
    :param http_proxy: URL HTTP-прокси (опционально, используется в loader.py)
    :param https_proxy: URL HTTPS-прокси (опционально)
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    telegram_token: str
    api_base_url: str
    request_timeout: int = 15
    debug: bool = False
    http_proxy: str | None = None
    https_proxy: str | None = None

    redis_host: str
    redis_password: str
    redis_db: int
    redis_port: int = 6379


bot_settings = BotSettings()
