import logging
import sys
from .constants import SERVER_NAME, DEFAULT_LOG_LEVEL, LSP_LOG_LEVELS


def setup_logging(level: str = DEFAULT_LOG_LEVEL, log_file: str | None = None) -> None:
    if level.upper() not in LSP_LOG_LEVELS:
        level = DEFAULT_LOG_LEVEL

    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        handlers=handlers,
        force=True,
    )

    logger = logging.getLogger(SERVER_NAME)
    logger.debug("Logging initialized at %s level", level)


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(f"{SERVER_NAME}.{name}" if name else SERVER_NAME)
