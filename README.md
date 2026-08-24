# 🎯 Чат-бот для трекинга привычек

Telegram-бот для отслеживания и формирования привычек. Бот помогает пользователям ставить цели, отслеживать прогресс, получать напоминания и вести статистику выполнения ежедневных задач.

## ✨ Возможности

- **Регистрация и авторизация** — безопасная аутентификация пользователей через Telegram с хешированием паролей и JWT-токенами
- **Управление привычками** — создание, редактирование, удаление привычек с указанием названия, описания, цели и срока выполнения
- **Ежедневный трекинг** — отметка выполнения/невыполнения привычек с автоматическим подсчётом прогресса
- **Напоминания** — установка времени напоминания для каждой привычки с учётом часового пояса пользователя
- **Статистика** — просмотр прогресса по каждой привычке (выполнено/цель, процент выполнения, статус на сегодня)
- **Перенос пропусков** — автоматический перенос невыполненных привычек на следующий день
- **Inline-меню** — удобное управление через inline-клавиатуры прямо в чате

## 🏗️ Архитектура

Проект построен по модульной архитектуре и разделён на два независимых компонента:

```
┌───────────────────────────────────────────────────────┐
│                     Docker Compose                    │
│                                                       │
│  ┌────────────┐      ┌───────────┐      ┌──────────┐  │
│  │    База    │◄─────│  Бэкенд   │◄─────│   Бот    │  │
│  │   данных   │      │ (FastAPI) │      │(Telegram)│  │
│  │(PostgreSQL)│      │           │      │          │  │
│  └────────────┘      └───────────┘      └──────────┘  │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### Backend (FastAPI)
- **REST API** для управления привычками, аутентификации и статистики
- **JWT-авторизация** с access и refresh токенами
- **SQLAlchemy + asyncpg** для асинхронной работы с PostgreSQL
- **Alembic** для управления миграциями БД
- **Планировщик задач** (APScheduler) для автоматического переноса привычек

### Bot (pyTelegramBotAPI)
- **pyTelegramBotAPI** для взаимодействия с Telegram API
- **FSM (Машина состояний)** для организации пошаговых диалогов с пользователем
- **APScheduler** для отправки напоминаний по расписанию
- **Token Storage** для хранения JWT-токенов пользователей в памяти
- **Inline-клавиатуры** для удобной навигации

### Хранилище данных
- **PostgreSQL** — основная база данных для пользователей, привычек и логов выполнения

## 🛠️ Технологический стек

| Компонент        | Технология                              |
|------------------|-----------------------------------------|
| Backend          | FastAPI, Uvicorn, SQLAlchemy, Alembic   |
| Bot              | pyTelegramBotAPI, APScheduler, requests |
| Database         | PostgreSQL, asyncpg                     |
| Auth             | python-jose (JWT), bcrypt               |
| Logging          | Loguru                                  |
| Containerization | Docker, Docker Compose                  |
| Python           | 3.14+                                   |

## 📁 Структура проекта

```
skillbox_chatbot_tracking_habits/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/                # API роутеры (auth, habits, user)
│   │   ├── core/               # Безопасность, зависимости
│   │   ├── models/             # SQLAlchemy модели (User, Habit, HabitLog)
│   │   ├── schemas/            # Pydantic схемы для валидации
│   │   ├── services/           # Бизнес-логика (auth, habits, user)
│   │   ├── utils/              # Утилиты (логирование)
│   │   ├── config.py           # Конфигурация (Pydantic Settings)
│   │   ├── database.py         # Подключение к БД
│   │   └── main.py             # Точка входа FastAPI
│   ├── alembic/                # Миграции базы данных
│   │   ├── versions/           # Файлы миграций
│   │   └── env.py              # Конфигурация Alembic
│   ├── pyproject.toml          # Зависимости (Poetry)
│   └── Dockerfile              # Конфигурация контейнера
├── bot/                        # Telegram bot
│   ├── api/                    # Клиент для REST API бэкенда
│   ├── handlers/               # Обработчики сообщений и callback-ов
│   ├── keyboards/              # Inline-клавиатуры
│   ├── services/               # Бизнес-логика бота (auth, habits, tracking)
│   ├── utils/                  # Утилиты (логирование)
│   ├── config.py               # Конфигурация бота
│   ├── loader.py               # Инициализация бота
│   ├── main.py                 # Точка входа
│   ├── notifier.py             # Планировщик напоминаний
│   ├── states.py               # FSM состояния
│   ├── storage.py              # Хранилище токенов
│   └── Dockerfile              # Конфигурация контейнера
├── docker-compose.yml          # Оркестрация контейнеров
├── .env.example                # Пример переменных окружения
└── README.md                   # Описание проекта
```

## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))

### Установка

1. **Клонировать репозиторий:**

```bash
git clone <repository-url>
cd skillbox_chatbot_tracking_habits
```

2. **Создать файл `.env`** на основе `.env.example` и заполнить значения:

```bash
cp .env.example .env
```

3. **Отредактировать `.env`** — указать ваши значения:

```env
# Database
POSTGRES_USER=habit_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_NAME=habit_db
POSTGRES_HOST=database
POSTGRES_PORT=5432

# JWT
SECRET_KEY=generate-a-long-random-secret-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

# Telegram Bot
TELEGRAM_TOKEN=your-telegram-bot-token
API_BASE_URL=http://backend:8000
REQUEST_TIMEOUT=15

# Proxy (опционально, если Telegram заблокирован)
HTTP_PROXY=socks5h://host.docker.internal:9150
HTTPS_PROXY=socks5h://host.docker.internal:9150

# Debug
DEBUG=True
```

4. **Запустить проект через Docker Compose:**

```bash
docker compose up --build
```

Контейнеры будут запущены:
- `habit_database` — PostgreSQL (порт 5432)
- `habit_backend` — FastAPI (порт 8000)
- `habit_bot` — Telegram бот

5. **Проверить запуск:**

- API документация: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Бот должен ответить на команду `/start` в Telegram

## 📋 Команды бота

| Команда         | Описание                                         |
|-----------------|--------------------------------------------------|
| `/start`        | Запуск бота, регистрация или показ главного меню |
| `/login`        | Вход для зарегистрированных пользователей        |
| `/add_habit`    | Добавить новую привычку                          |
| `/habits`       | Показать список всех привычек                    |
| `/edit_habit`   | Редактировать привычку                           |
| `/delete_habit` | Удалить привычку                                 |
| `/set_reminder` | Установить напоминание для привычки              |
| `/habit_stats`  | Просмотр статистики по привычке                  |
| `/track_habit`  | Отметить выполнение привычки                     |
| `/help`         | Справка по командам                              |

## 🔌 API Endpoints

### Аутентификация
| Метод   | Путь                | Описание                        | Авторизация   |
|---------|---------------------|---------------------------------|---------------|
| POST    | `/auth/register`    | Регистрация нового пользователя | Нет           |
| POST    | `/auth/login`       | Вход по Telegram ID и паролю    | Нет           |
| POST    | `/auth/login/oauth` | Вход через OAuth2 форму         | Нет           |
| POST    | `/auth/refresh`     | Обновление access-токена        | Нет           |

### Привычки
| Метод   | Путь                 | Описание                 | Авторизация   |
|---------|----------------------|--------------------------|---------------|
| POST    | `/habits`            | Создать новую привычку   | Bearer JWT    |
| GET     | `/habits`            | Получить список привычек | Bearer JWT    |
| GET     | `/habits/{id}`       | Получить привычку по ID  | Bearer JWT    |
| PATCH   | `/habits/{id}`       | Редактировать привычку   | Bearer JWT    |
| DELETE  | `/habits/{id}`       | Удалить привычку         | Bearer JWT    |
| POST    | `/habits/{id}/track` | Отметить выполнение      | Bearer JWT    |
| GET     | `/habits/{id}/stats` | Получить статистику      | Bearer JWT    |

### Внутренние (для бота)
| Метод   | Путь                          | Описание                          | Авторизация   |
|---------|-------------------------------|-----------------------------------|---------------|
| POST    | `/habits/internal/carry-over` | Перенос невыполненных привычек    | Нет           |
| GET     | `/habits/internal/reminders`  | Получить привычки для напоминания | Нет           |

### Пользователь
| Метод   | Путь       | Описание                               | Авторизация   |
|---------|------------|----------------------------------------|---------------|
| GET     | `/user/me` | Получить профиль текущего пользователя | Bearer JWT    |

## 🗄️ Модели данных

### User
| Поле            | Тип         | Описание                               |
|-----------------|-------------|----------------------------------------|
| id              | Integer     | Первичный ключ                         |
| telegram_id     | Integer     | Telegram ID пользователя (уникальный)  |
| username        | String(255) | Имя пользователя в Telegram (nullable) |
| full_name       | String(255) | Полное имя                             |
| hashed_password | String(255) | Хеш пароля                             |
| timezone        | String(64)  | Часовой пояс (по умолчанию UTC)        |
| refresh_token   | String(512) | Refresh-токен (nullable)               |
| created_at      | DateTime    | Дата создания                          |

### Habit
| Поле               | Тип         | Описание                                  |
|--------------------|-------------|-------------------------------------------|
| id                 | Integer     | Первичный ключ                            |
| user_id            | Integer     | FK → users.id                             |
| title              | String(255) | Название привычки                         |
| description        | Text        | Описание (nullable)                       |
| target_description | Text        | Цель (nullable)                           |
| target_days        | Integer     | Целевое количество дней (по умолчанию 21) |
| completed_count    | Integer     | Количество выполнений                     |
| is_active          | Boolean     | Активна ли привычка                       |
| reminder_time      | Time        | Время напоминания (nullable)              |
| created_at         | DateTime    | Дата создания                             |

### HabitLog
| Поле         | Тип      | Описание       |
|--------------|----------|----------------|
| id           | Integer  | Первичный ключ |
| habit_id     | Integer  | FK → habits.id |
| log_date     | Date     | Дата отметки   |
| is_completed | Boolean  | Выполнено/нет  |
| created_at   | DateTime | Дата создания  |

## ⚙️ Конфигурация

Все настройки хранятся в файле `.env` (см. `.env.example`).

### Основные переменные

| Переменная                    | По умолчанию        | Описание                           |
|-------------------------------|---------------------|------------------------------------|
| `POSTGRES_USER`               | —                   | Пользователь БД                    |
| `POSTGRES_PASSWORD`           | —                   | Пароль БД                          |
| `POSTGRES_NAME`               | —                   | Имя БД                             |
| `POSTGRES_HOST`               | localhost           | Хост БД                            |
| `POSTGRES_PORT`               | 5432                | Порт БД                            |
| `SECRET_KEY`                  | —                   | Секретный ключ для JWT             |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30                  | Время жизни access-токена (минуты) |
| `REFRESH_TOKEN_EXPIRE_DAYS`   | 30                  | Время жизни refresh-токена (дни)   |
| `TELEGRAM_TOKEN`              | —                   | Токен Telegram-бота                |
| `API_BASE_URL`                | http://backend:8000 | URL бэкенда                        |
| `HTTP_PROXY`                  | —                   | HTTP-прокси (опционально)          |
| `HTTPS_PROXY`                 | —                   | HTTPS-прокси (опционально)         |
| `DEBUG`                       | False               | Режим отладки                      |

## 📝 Логирование

Логирование реализовано с помощью **Loguru** в обоих компонентах:

- **Backend:** логи в `backend/logs/backend_*.log`
- **Bot:** логи в `bot/logs/bot_*.log`
- **Уровень:** INFO (DEBUG если `DEBUG=True`)
- **Ротация:** 10 MB
- **Хранение:** 14 дней
- **Сжатие:** ZIP

## 🔄 Планировщик задач

### Перенос привычек (Backend)
- **Расписание:** ежедневно в 23:59 UTC
- **Логика:** все активные привычки, не отмеченные как выполненные сегодня, переносятся на следующий день. Привычки, достигшие цели, деактивируются.

### Напоминания (Bot)
- **Расписание:** каждую минуту
- **Логика:** бот запрашивает привычки, у которых `reminder_time` совпадает с текущим временем (в UTC), и отправляет уведомления пользователям.

## 📦 Управление

### Остановка
```bash
docker compose down
```

### Остановка с удалением данных БД
```bash
docker compose down -v
```

### Просмотр логов
```bash
# Все сервисы
docker compose logs -f

# Только бот
docker compose logs -f bot

# Только бэкенд
docker compose logs -f backend
```

### Пересоздание контейнеров
```bash
docker compose up --build
```

### Миграции БД (Alembic)
Миграции применяются автоматически при запуске бэкенда. Для ручного управления:

```bash
# Создать новую миграцию
docker compose exec backend alembic revision --autogenerate -m "description"

# Применить миграции
docker compose exec backend alembic upgrade head

# Откатить последнюю миграцию
docker compose exec backend alembic downgrade -1
```
