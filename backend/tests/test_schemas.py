"""
Тесты Pydantic-схем валидации
"""

import datetime

import pytest
from pydantic import ValidationError

from app.schemas.habit_schema import (
    HabitCreate,
    HabitStats,
    HabitTrackRequest,
    HabitUpdate,
)
from backend.app.schemas.user_schema import UserCreate, UserLogin


class TestUserCreate:
    def test_valid_user_create(self):
        user = UserCreate(
            telegram_id=123456,
            full_name="Иван Иванов",
            password="secret123",
        )
        assert user.telegram_id == 123456
        assert user.username is None

    def test_short_password_raises(self):
        with pytest.raises(ValidationError):
            UserCreate(
                telegram_id=123456,
                full_name="Иван",
                password="12345",
            )

    def test_empty_full_name_raises(self):
        with pytest.raises(ValidationError):
            UserCreate(
                telegram_id=123456,
                full_name="",
                password="secret123",
            )

    def test_with_username(self):
        user = UserCreate(
            telegram_id=123456,
            full_name="Иван",
            password="secret123",
            username="ivan_dev",
        )
        assert user.username == "ivan_dev"


class TestUserLogin:
    def test_valid_login(self):
        login = UserLogin(telegram_id=123, password="secret123")
        assert login.telegram_id == 123

    def test_missing_password_raises(self):
        with pytest.raises(ValidationError):
            UserLogin(telegram_id=123)


class TestHabitCreate:
    def test_valid_habit_create(self):
        habit = HabitCreate(title="Пить воду")
        assert habit.title == "Пить воду"
        assert habit.target_days == 21
        assert habit.reminder_time is None

    def test_empty_title_raises(self):
        with pytest.raises(ValidationError):
            HabitCreate(title="")

    def test_target_days_too_large_raises(self):
        with pytest.raises(ValidationError):
            HabitCreate(title="Test", target_days=366)

    def test_target_days_zero_raises(self):
        with pytest.raises(ValidationError):
            HabitCreate(title="Test", target_days=0)

    def test_with_reminder_time(self):
        habit = HabitCreate(
            title="Бегать",
            reminder_time=datetime.time(9, 30),
        )
        assert habit.reminder_time == datetime.time(9, 30)


class TestHabitUpdate:
    def test_all_fields_none_by_default(self):
        habit = HabitUpdate()
        assert habit.title is None
        assert habit.description is None
        assert habit.target_days is None

    def test_partial_update(self):
        habit = HabitUpdate(title="Новое название")
        assert habit.title == "Новое название"
        assert habit.description is None

    def test_target_days_validation(self):
        with pytest.raises(ValidationError):
            HabitUpdate(target_days=400)


class TestHabitTrackRequest:
    def test_valid_track_request(self):
        req = HabitTrackRequest(is_completed=True)
        assert req.is_completed is True
        assert req.log_date is None

    def test_with_log_date(self):
        req = HabitTrackRequest(
            is_completed=False,
            log_date=datetime.date(2026, 1, 1),
        )
        assert req.log_date == datetime.date(2026, 1, 1)


class TestHabitStats:
    def test_valid_stats(self):
        stats = HabitStats(
            habit_id=1,
            title="Test",
            completed_count=5,
            target_days=21,
            progress_percent=23.81,
            is_completed_today=True,
        )
        assert stats.progress_percent == 23.81
