"""
Настройка подключения к базе данных и базовый класс моделей.

Содержит асинхронный движок SQLAlchemy, фабрику сессий и функцию-зависимость
для получения сессии в маршрутах FastAPI.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from .config import get_settings

settings = get_settings()

async_engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)
async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy в приложении.

    Все модели наследуются от этого класса, чтобы быть зарегистрированными
    в метаданных Base.metadata, используемых Alembic для миграций.
    """

    __abstract__ = True


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Возвращает асинхронный генератор сессий БД для FastAPI.

    Создаёт новую сессию, отдаёт её в маршрут, а затем автоматически
    выполняет коммит при успехе или откат (rollback) при возникновении ошибки.

    :return: Асинхронный генератор, yielding объект AsyncSession
    :rtype: AsyncGenerator[AsyncSession, None]
    """

    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
