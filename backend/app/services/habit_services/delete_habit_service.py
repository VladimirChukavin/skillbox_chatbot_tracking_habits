"""
Сервис для удаления привычки.

Содержит функцию для безвозвратного удаления привычки и связанных
с ней логов выполнения из базы данных.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_model import Habit


async def delete_habit(session: AsyncSession, habit: Habit) -> None:
    """
    Удалить привычку из базы данных.

    Удаление происходит с каскадным удалением связанных записей
    в таблице логов выполнения (благодаря настройкам модели).

    :param session: Асинхронная сессия БД
    :type session: AsyncSession
    :param habit: Объект удаляемой привычки
    :type habit: Habit
    :return: Ничего не возвращает
    :rtype: None
    """

    await session.delete(habit)
    await session.flush()
