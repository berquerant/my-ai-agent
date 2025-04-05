import logging
import sys
from typing import cast


__logger: None | logging.Logger = None


def init(log_level: int) -> None:
    """Initialize the logger."""
    global __logger, __level
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )
    __logger = logging.getLogger(__name__)
    __logger.setLevel(log_level)


def __get() -> logging.Logger:
    return cast(logging.Logger, __logger)


def log() -> logging.Logger:
    """Return the logger instance."""
    return __get()
