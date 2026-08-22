from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from .config import get_settings

from .api.router import main_router
from .utils.logger import configure_logger

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
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
    return {"status": "ok"}
