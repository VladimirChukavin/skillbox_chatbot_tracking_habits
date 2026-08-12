import asyncio
import datetime

import requests
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from bot.config import bot_settings
from bot.storage import token_storage


class HabitNotifier:
    CARRY_OVER_ENDPOINT = "/habits/internal/carry-over"
    HABITS_ENDPOINT = "/habits/"

    def __init__(self, bot, scheduler: AsyncIOScheduler | None = None) -> None:
        self._bot = bot
        self._scheduler = scheduler or AsyncIOScheduler(timezone="UTC")
        self._api_base_url = bot_settings.api_base_url.rstrip("/")

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

    async def run_carry_over(self) -> None:
        try:
            response = requests.post(
                f"{self._api_base_url}{self.CARRY_OVER_ENDPOINT}",
                timeout=bot_settings.request_timeout,
            )
            if response.status_code == 200:
                logger.info("Перенос привычек выполнен: {}", response.json())
            else:
                logger.warning("Перенос привычек: статус {}", response.status_code)
        except Exception as error:
            logger.exception("Ошибка при переносе привычек: {}", error)

    async def check_and_send_reminders(self) -> None:
        now = datetime.datetime.now(pytz.UTC)
        current_time = now.strftime("%H:%M")
        logger.info("Проверка напоминаний для времени {}", current_time)

    def stop(self) -> None:
        self._scheduler.shutdown(wait=False)
        logger.info("Планировщик оповещений остановлен.")
