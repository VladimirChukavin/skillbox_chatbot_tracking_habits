"""
Фоновый планировщик напоминаний и переноса привычек.

Содержит класс, который использует APScheduler
для выполнения периодических задач: ежедневный перенос
невыполненных привычек на следующий день и отправка
пользователям напоминаний по расписанию.
"""

import datetime

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from bot.config import bot_settings


class HabitNotifier:
    """
    Планировщик напоминаний и переноса привычек.

    Управляет двумя cron-задачами через BackgroundScheduler
    (часовой пояс UTC): перенос невыполненных привычек на следующий
    день и отправка напоминаний. Взаимодействует с backend API
    через requests.Session с отключённым чтением прокси из
    окружения (trust_env = False).

    :param CARRY_OVER_ENDPOINT: Endpoint API для переноса привычек
    :param HABITS_REMINDER_ENDPOINT: Endpoint API для получения
        активных напоминаний
    """

    CARRY_OVER_ENDPOINT = "/habits/internal/carry-over"
    HABITS_REMINDER_ENDPOINT = "/habits/internal/reminders"

    def __init__(self, bot, scheduler: BackgroundScheduler | None = None) -> None:
        """
        Инициализировать планировщик оповещений.

        Сохраняет ссылку на экземпляр бота для отправки сообщений,
        создаёт или принимает внешний BackgroundScheduler
        (часовой пояс UTC), формирует базовый URL API из
        bot_settings.api_base_url и инициализирует
        requests.Session с trust_env = False для обхода
        системных прокси-настроек.

        :param bot: Экземпляр Telegram-бота для отправки сообщений
        :param scheduler: Внешний планировщик APScheduler (опционально).
            Если не передан — создаётся новый с часовым поясом UTC.
        :type scheduler: BackgroundScheduler | None
        :return: Ничего не возвращает
        :rtype: None
        """

        self._bot = bot
        self._scheduler = scheduler or BackgroundScheduler(timezone="UTC")
        self._api_base_url = bot_settings.api_base_url.rstrip("/")
        self._session = requests.Session()
        self._session.trust_env = False

    def start(self) -> None:
        """
        Запустить планировщик оповещений.

        Добавляет две cron-задачи в планировщик:
        1. Перенос привычек (run_carry_over) — срабатывает
           ежедневно в 23:59 UTC.
        2. Отправка напоминаний (check_and_send_reminders) —
           срабатывает каждую минуту, равную началу часа
           (CronTrigger(minute=0)).

        Обе задачи регистрируются с replace_existing=True,
        что позволяет безопасно перезапускать планировщик без
        дублирования задач. Запускает планировщик методом
        start и записывает событие в лог.

        :return: Ничего не возвращает
        :rtype: None
        """

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
        """
        Перенести невыполненные привычки на следующий день.

        Отправляет POST-запрос на endpoint CARRY_OVER_ENDPOINT
        с таймаутом из bot_settings.request_timeout. При
        статусе 200 записывает результат в лог на уровне INFO.
        При любом другом статусе — предупреждение на уровне WARNING.
        В случае исключения записывает полный traceback через
        logger.exception.

        :return: Ничего не возвращает
        :rtype: None
        """

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
        """
        Проверить и отправить напоминания пользователям.

        Определяет текущее время в UTC в формате ЧЧ:ММ и
        отправляет GET-запрос на endpoint HABITS_REMINDER_ENDPOINT
        с параметром time. Если статус ответа не 200 —
        записывает предупреждение и прерывает выполнение.

        При успехе итерируется по списку напоминаний из ответа.
        Для каждого напоминания извлекает user_telegram_id и
        title, отправляет пользователю сообщение через бота и
        записывает событие в лог с привязкой sent_message=True
        (фильтруется отдельным файловым обработчиком из
        configure_bot_logger).

        В случае исключения записывает полный traceback через
        logger.exception.

        :return: Ничего не возвращает
        :rtype: None
        """

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
        """
        Остановить планировщик оповещений.

        Вызывает shutdown(wait=False) на планировщике, что
        немедленно прекращает выполнение задач без ожидания
        завершения уже запущенных. Записывает событие в лог.

        :return: Ничего не возвращает
        :rtype: None
        """

        self._scheduler.shutdown(wait=False)
        logger.info("Планировщик оповещений остановлен.")
