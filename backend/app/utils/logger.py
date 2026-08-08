import sys

from loguru import logger


def configure_logger(debug: bool = False) -> None:
    logger.remove()
    log_level = "DEBUG" if debug else "INFO"
    logger.add(
        sys.stdout,
        level=log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
    )
    logger.add(
        "logs/backend_{time}.log",
        level=log_level,
        rotation="10 MB",
        retention="14 days",
        compression="zip",
        encoding="utf-8",
    )
