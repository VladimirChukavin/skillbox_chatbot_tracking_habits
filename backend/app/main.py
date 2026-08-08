from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from .config import get_settings
from .routers import auth_router, habits_router, user_router
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


app.include_router(auth_router.router)
app.include_router(habits_router.router)
app.include_router(user_router.router)


@app.get("/health", tags=["service"])
async def check_health() -> dict[str, str]:
    return {"status": "ok"}
