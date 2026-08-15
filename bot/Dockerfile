FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN pip install --no-cache-dir \
    pyTelegramBotAPI==4.36.0 \
    requests[socks]==2.34.2 \
    loguru==0.7.3 \
    APScheduler==3.11.3 \
    pydantic-settings==2.14.2 \
    pytz==2026.3.post1

COPY . .

CMD ["python", "-m", "bot.main"]