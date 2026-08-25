"""
Тесты сервисных функций backend (с моками БД).
"""

import datetime
from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from app.models.habit_model import Habit
from app.models.habit_log_model import HabitLog
from app.models.user_model import User
from app.schemas.habit_schema import HabitCreate, HabitUpdate
from app.services.user_services.create_user_service import create_user
from app.core.security import hash_password
from app.services.auth_service import authenticate_user
from app.services.habit_services.create_habit_service import create_habit
from app.services.habit_services.track_habit_service import track_habit
from app.services.habit_services.calculate_habit_stats_service import (
    calculate_habit_stats,
)
from app.services.habit_services.carry_over_incomplete_habits_service import (
    carry_over_incomplete_habits,
)
from app.services.habit_services.update_habit_service import update_habit


@pytest.mark.asyncio
class TestCreateUser:
    async def test_create_user_success(self, mock_session):
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        user = await create_user(
            mock_session,
            telegram_id=123,
            full_name="Иван",
            password="secret123",
        )

        assert user.telegram_id == 123
        assert user.full_name == "Иван"
        assert user.hashed_password != "secret123"
        mock_session.add.assert_called_once()

    async def test_create_user_duplicate_raises(self, mock_session):
        existing_user = User(telegram_id=123, full_name="Старый", hashed_password="x")
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_user
        mock_session.execute.return_value = mock_result

        with pytest.raises(ValueError, match="уже существует"):
            await create_user(
                mock_session,
                telegram_id=123,
                full_name="Иван",
                password="secret123",
            )


@pytest.mark.asyncio
class TestAuthenticateUser:
    async def test_authenticate_success(self, mock_session):
        user = User(
            telegram_id=123,
            full_name="Иван",
            hashed_password=hash_password("secret123"),
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = user
        mock_session.execute.return_value = mock_result

        result = await authenticate_user(mock_session, 123, "secret123")
        assert result is not None
        assert result.telegram_id == 123

    async def test_authenticate_wrong_password(self, mock_session):
        user = User(
            telegram_id=123,
            full_name="Иван",
            hashed_password=hash_password("secret123"),
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = user
        mock_session.execute.return_value = mock_result

        result = await authenticate_user(mock_session, 123, "wrong")
        assert result is None

    async def test_authenticate_user_not_found(self, mock_session):
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await authenticate_user(mock_session, 999, "secret123")
        assert result is None


@pytest.mark.asyncio
class TestCreateHabit:
    async def test_create_habit_without_reminder(self, mock_session):
        user = User(
            telegram_id=123, full_name="Иван", hashed_password="x", timezone="UTC"
        )
        payload = HabitCreate(title="Пить воду", target_days=30)

        habit = await create_habit(mock_session, user_id=1, payload=payload, user=user)

        assert habit.title == "Пить воду"
        assert habit.target_days == 30
        assert habit.reminder_time is None
        mock_session.add.assert_called_once()

    async def test_create_habit_with_reminder_timezone(self, mock_session):
        user = User(
            telegram_id=123,
            full_name="Иван",
            hashed_password="x",
            timezone="Europe/Moscow",
        )
        payload = HabitCreate(
            title="Бегать",
            reminder_time=datetime.time(9, 30),
        )

        habit = await create_habit(mock_session, user_id=1, payload=payload, user=user)

        assert habit.reminder_time is not None
        assert habit.reminder_time.hour == 6
        assert habit.reminder_time.minute == 30


@pytest.mark.asyncio
class TestTrackHabit:
    async def test_track_new_completed(self, mock_session):
        habit = Habit(id=1, user_id=1, title="Test", target_days=21, completed_count=0)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        log = await track_habit(mock_session, habit, is_completed=True)

        assert log.is_completed is True
        assert habit.completed_count == 1

    async def test_track_new_not_completed(self, mock_session):
        habit = Habit(id=1, user_id=1, title="Test", target_days=21, completed_count=0)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        log = await track_habit(mock_session, habit, is_completed=False)

        assert log.is_completed is False
        assert habit.completed_count == 0

    async def test_track_change_to_completed(self, mock_session):
        habit = Habit(id=1, user_id=1, title="Test", target_days=21, completed_count=0)
        existing_log = HabitLog(
            habit_id=1, log_date=datetime.date.today(), is_completed=False
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_log
        mock_session.execute.return_value = mock_result

        log = await track_habit(mock_session, habit, is_completed=True)

        assert log.is_completed is True
        assert habit.completed_count == 1

    async def test_track_change_to_not_completed(self, mock_session):
        habit = Habit(id=1, user_id=1, title="Test", target_days=21, completed_count=5)
        existing_log = HabitLog(
            habit_id=1, log_date=datetime.date.today(), is_completed=True
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_log
        mock_session.execute.return_value = mock_result

        log = await track_habit(mock_session, habit, is_completed=False)

        assert log.is_completed is False
        assert habit.completed_count == 4

    async def test_track_completed_not_below_zero(self, mock_session):
        habit = Habit(id=1, user_id=1, title="Test", target_days=21, completed_count=0)
        existing_log = HabitLog(
            habit_id=1, log_date=datetime.date.today(), is_completed=True
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_log
        mock_session.execute.return_value = mock_result

        await track_habit(mock_session, habit, is_completed=False)

        assert habit.completed_count == 0


@pytest.mark.asyncio
class TestCalculateHabitStats:
    async def test_stats_no_long_today(self, mock_session):
        habit = Habit(id=1, user_id=1, title="Test", target_days=21, completed_count=5)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        stats = await calculate_habit_stats(habit, mock_session)

        assert stats["habit_id"] == 1
        assert stats["completed_count"] == 5
        assert stats["target_days"] == 21
        assert stats["progress_percent"] == round(5 / 21 * 100, 2)
        assert stats["is_completed_today"] is False

    async def test_stats_completed_today(self, mock_session):
        habit = Habit(id=1, user_id=1, title="Test", target_days=21, completed_count=5)
        log_entry = HabitLog(
            habit_id=1, log_date=datetime.date.today(), is_completed=True
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = log_entry
        mock_session.execute.return_value = mock_result

        stats = await calculate_habit_stats(habit, mock_session)

        assert stats["is_completed_today"] is True

    async def test_stats_zero_target_days(self, mock_session):
        habit = Habit(id=1, user_id=1, title="Test", target_days=0, completed_count=0)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        stats = await calculate_habit_stats(habit, mock_session)

        assert stats["progress_percent"] == 0


@pytest.mark.asyncio
class TestCarryOverIncompleteHabits:
    async def test_create_log_for_incomplete_habits(self, mock_session):
        habit = Habit(
            id=1,
            user_id=1,
            title="Test",
            target_days=21,
            completed_count=0,
            is_active=True,
        )

        list_result = MagicMock()
        list_result.scalars.return_value = [habit]

        log_check_result = MagicMock()
        log_check_result.scalar_one_or_none.return_value = None

        mock_session.execute.side_effect = [list_result, log_check_result]

        count = await carry_over_incomplete_habits(mock_session)

        assert count == 1
        assert mock_session.execute.call_count == 2

    async def test_deactivate_completed_habits(self, mock_session):
        habit = Habit(
            id=1,
            user_id=1,
            title="Test",
            target_days=21,
            completed_count=21,
            is_active=True,
        )

        list_result = MagicMock()
        list_result.scalars.return_value = [habit]

        mock_session.execute.side_effect = [list_result]

        count = await carry_over_incomplete_habits(mock_session)

        assert count == 0
        assert habit.is_active is False


@pytest.mark.asyncio
class TestUpdateHabit:
    async def test_update_title_only(self, mock_session):
        habit = Habit(
            id=1, user_id=1, title="Старое", target_days=21, completed_count=0
        )
        user = User(
            telegram_id=123, full_name="Иван", hashed_password="x", timezone="UTC"
        )
        payload = HabitUpdate(title="Новое название")

        updated = await update_habit(mock_session, habit, payload, user)

        assert updated.title == "Новое название"

    async def test_update_reminder_time_timezone(self, mock_session):
        habit = Habit(id=1, user_id=1, title="Test", target_days=21, completed_count=0)
        user = User(
            telegram_id=123,
            full_name="Иван",
            hashed_password="x",
            timezone="Europe/Moscow",
        )
        payload = HabitUpdate(reminder_time=datetime.time(9, 30))

        updated = await update_habit(mock_session, habit, payload, user)

        assert updated.reminder_time is not None
        assert updated.reminder_time.hour == 6
