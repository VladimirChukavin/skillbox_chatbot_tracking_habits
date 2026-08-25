"""
Тесты функций построения inline-клавиатур.
"""

from telebot.types import InlineKeyboardMarkup

from bot.keyboards.edit_fields_keyboard import build_edit_fields_keyboard
from bot.keyboards.habits_keyboard import build_habits_keyboard
from bot.keyboards.main_menu_keyboard import build_main_menu_keyboard
from bot.keyboards.track_keyboard import build_track_keyboard


class TestMainMenuKeyboard:
    def test_returns_inline_markup(self):
        kb = build_main_menu_keyboard()
        assert isinstance(kb, InlineKeyboardMarkup)

    def test_contains_add_button(self):
        kb = build_main_menu_keyboard()
        all_callbacks = [btn.callback_data for row in kb.keyboard for btn in row]
        assert "menu:add" in all_callbacks

    def test_contains_list_button(self):
        kb = build_main_menu_keyboard()
        all_callbacks = [btn.callback_data for row in kb.keyboard for btn in row]
        assert "menu:list" in all_callbacks

    def test_contains_delete_button(self):
        kb = build_main_menu_keyboard()
        all_callbacks = [btn.callback_data for row in kb.keyboard for btn in row]
        assert "menu:delete" in all_callbacks

    def test_all_callbacks_start_with_menu(self):
        kb = build_main_menu_keyboard()
        all_callbacks = [btn.callback_data for row in kb.keyboard for btn in row]
        assert all(cb.startswith("menu:") for cb in all_callbacks)


class TestHabitsKeyboard:
    def test_empty_list(self):
        kb = build_habits_keyboard([], callback_prefix="edit")
        assert isinstance(kb, InlineKeyboardMarkup)
        assert len(kb.keyboard) == 0

    def test_single_habit(self):
        habits = [{"id": 1, "title": "Пить воду"}]
        kb = build_habits_keyboard(habits, callback_prefix="edit")
        assert len(kb.keyboard) == 1
        assert kb.keyboard[0][0].callback_data == "edit:1"
        assert kb.keyboard[0][0].text == "Пить воду"

    def test_multiple_habits(self):
        habits = [
            {"id": 1, "title": "Пить воду"},
            {"id": 2, "title": "Бегать"},
        ]
        kb = build_habits_keyboard(habits, callback_prefix="delete")
        assert len(kb.keyboard) == 2
        assert kb.keyboard[0][0].callback_data == "delete:1"
        assert kb.keyboard[1][0].callback_data == "delete:2"

    def test_different_prefix(self):
        habits = [{"id": 5, "title": "Test"}]
        kb = build_habits_keyboard(habits, callback_prefix="track")
        assert kb.keyboard[0][0].callback_data == "track:5"


class TestTrackKeyboard:
    def test_returns_inline_markup(self):
        kb = build_track_keyboard(habit_id=1)
        assert isinstance(kb, InlineKeyboardMarkup)

    def test_has_two_buttons(self):
        kb = build_track_keyboard(habit_id=1)
        assert len(kb.keyboard) == 1
        assert len(kb.keyboard[0]) == 2

    def test_done_callback(self):
        kb = build_track_keyboard(habit_id=42)
        assert kb.keyboard[0][0].callback_data == "track_done:42"

    def test_skip_callback(self):
        kb = build_track_keyboard(habit_id=42)
        assert kb.keyboard[0][1].callback_data == "track_skip:42"


class TestEditFieldsKeyboard:
    def test_returns_inline_markup(self):
        kb = build_edit_fields_keyboard()
        assert isinstance(kb, InlineKeyboardMarkup)

    def test_has_five_buttons(self):
        kb = build_edit_fields_keyboard()
        all_callbacks = [btn.callback_data for row in kb.keyboard for btn in row]
        assert len(all_callbacks) == 5

    def test_contains_title_field(self):
        kb = build_edit_fields_keyboard()
        all_callbacks = [btn.callback_data for row in kb.keyboard for btn in row]
        assert "field:title" in all_callbacks

    def test_contains_delete_field(self):
        kb = build_edit_fields_keyboard()
        all_callbacks = [btn.callback_data for row in kb.keyboard for btn in row]
        assert "field:delete" in all_callbacks

    def test_all_callbacks_start_with_field(self):
        kb = build_edit_fields_keyboard()
        all_callbacks = [btn.callback_data for row in kb.keyboard for btn in row]
        assert all(cb.startswith("field:") for cb in all_callbacks)
