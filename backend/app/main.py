"""
Точка входа для FastAPI-приложения бэкенда.

Содержит инициализацию приложения, настройку логирования через lifespan,
подключение основного роутера и health-check endpoint.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from .config import get_settings

from .api.router import main_router
from .utils.logger import configure_logger

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер жизненного цикла приложения.

    Выполняет настройку логгера при запуске и логирует остановку при завершении.

    :param app: Экземпляр приложения FastAPI
    :type app: FastAPI
    :yield: Передает управление приложению во время его работы
    """

    configure_logger(debug=settings.debug)
    logger.info("Запуск FastAPI-приложения для трекинга привычек")
    yield
    logger.info("Остановка FastAPI-приложения")


app = FastAPI(
    title="Habit tracker API",
    description="Бэкенд чат-бота для трекинга привычек",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(main_router)


@app.get("/health", tags=["service"])
async def check_health() -> dict[str, str]:
    """
    Проверить работоспособность приложения.

    Используется для health-checks (например, в Docker Compose).

    :return: Словарь со статусом приложения
    :rtype: dict[str, str]
    """

    return {"status": "ok"}
