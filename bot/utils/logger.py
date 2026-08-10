import sys

from loguru import logger


def configure_bot_logger(debug: bool = False) -> None:
    logger.remove()
    log_level = "DEBUG" if debug else "INFO"
    logger.add(
        sys.stdout,
        level=log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | <cyan>{name}</cyan> | <level>{message}</level>"
        ),
    )
    logger.add(
        "logs/bot_{time}.log",
        level=log_level,
        rotation="10 MB",
        retention="14 days",
        compression="zip",
        encoding="utf-8",
    )
    logger.add(
        "logs/bot_sent_messages.log",
        level="INFO",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
        filter=lambda record: "sent_messages" in record["extra"],
    )
