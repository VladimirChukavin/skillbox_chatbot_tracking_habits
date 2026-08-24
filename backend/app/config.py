"""
Конфигурация приложения на основе Pydantic Settings.

Содержит класс настроек, который считывает переменные окружения из файла .env,
и функцию для получения единственного экземпляра конфигурации (кэшируется).
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки приложения.

    Все переменные считываются из окружения (файла .env).

    :param postgres_user: Имя пользователя БД PostgreSQL
    :param postgres_password: Пароль пользователя БД
    :param postgres_name: Название базы данных
    :param postgres_host: Хост БД (по умолчанию "localhost")
    :param postgres_port: Порт БД (по умолчанию 5432)
    :param secret_key: Секретный ключ для генерации JWT-токенов
    :param algorithm: Алгоритм хеширования JWT (по умолчанию "HS256")
    :param access_token_expire_minutes: Время жизни access-токена в минутах (по умолчанию 30)
    :param refresh_token_expire_days: Время жизни refresh-токена в днях (по умолчанию 30)
    :param debug: Флаг режима отладки (по умолчанию False)
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    postgres_user: str
    postgres_password: str
    postgres_name: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30

    debug: bool = False

    @property
    def database_url(self) -> str:
        """
        Строка подключения к БД для асинхронного драйвера (asyncpg).

        :return: DSN для PostgreSQL (asyncpg)
        :rtype: str
        """

        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_name}"
        )

    @property
    def sync_database_url(self) -> str:
        """
        Строка подключения к БД для синхронного драйвера (psycopg2).

        Используется инструментами миграции (Alembic).

        :return: DSN для PostgreSQL (psycopg2)
        :rtype: str
        """

        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_name}"
        )


@lru_cache
def get_settings() -> Settings:
    """
    Возвращает singleton-экземпляр настроек приложения.

    Благодаря декоратору lru_cache объект Settings
    создаётся только один раз за весь жизненный цикл приложения.

    :return: Экземпляр настроек
    :rtype: Settings
    """

    return Settings()
