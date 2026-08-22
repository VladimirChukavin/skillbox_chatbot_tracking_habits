import datetime

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from bot.config import bot_settings


class HabitNotifier:
    CARRY_OVER_ENDPOINT = "/habits/internal/carry-over"
    HABITS_REMINDER_ENDPOINT = "/habits/internal/reminders"

    def __init__(self, bot, scheduler: BackgroundScheduler | None = None) -> None:
        self._bot = bot
        self._scheduler = scheduler or BackgroundScheduler(timezone="UTC")
        self._api_base_url = bot_settings.api_base_url.rstrip("/")
        self._session = requests.Session()
        self._session.trust_env = False

    def start(self) -> None:
        self._scheduler.add_job(
            self.run_carry_over,
            CronTrigger(hour=23, minute=59),
            id="carry_over_habits",
            replace_existing=True,
        )
        self._scheduler.add_job(
            self.check_and_send_reminders,
            CronTrigger(minute=0),
            id="send_reminders",
            replace_existing=True,
        )
        self._scheduler.start()
        logger.info("Планировщик оповещений запущен.")

    def run_carry_over(self) -> None:
        try:
            response = self._session.post(
                f"{self._api_base_url}{self.CARRY_OVER_ENDPOINT}",
                timeout=bot_settings.request_timeout,
            )
            if response.status_code == 200:
                logger.info("Перенос привычек выполнен: {}", response.json())
            else:
                logger.warning("Перенос привычек: статус {}", response.status_code)
        except Exception as error:
            logger.exception("Ошибка при переносе привычек: {}", error)

    def check_and_send_reminders(self) -> None:
        now = datetime.datetime.now(datetime.timezone.utc)
        current_time = now.strftime("%H:%M")
        logger.info("Проверка напоминаний для времени {}", current_time)

        try:
            response = self._session.get(
                f"{self._api_base_url}{self.HABITS_REMINDER_ENDPOINT}",
                params={"time": current_time},
                timeout=bot_settings.request_timeout,
            )

            if response.status_code != 200:
                logger.warning(
                    "Не удалось получить напоминание: {}", response.status_code
                )
                return

            reminders = response.json()

            for reminder in reminders:
                telegram_id = reminder.get("user_telegram_id")
                habit_title = reminder.get("title")
                self._bot.send_message(
                    telegram_id,
                    f'⏰ Напоминание! Пора выполнить привычку "{habit_title}"',
                )
                logger.bind(sent_message=True).info(
                    "Отправлено напоминание пользователю {} по привычке {}",
                    telegram_id,
                    habit_title,
                )
        except Exception as error:
            logger.exception("Ошибка при отправке напоминаний: {}", error)

    def stop(self) -> None:
        self._scheduler.shutdown(wait=False)
        logger.info("Планировщик оповещений остановлен.")
