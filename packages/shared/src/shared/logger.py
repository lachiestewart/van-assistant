"""Logging utilities for the van assistant system."""

import logging

from pythonjsonlogger.json import JsonFormatter

LOG_LEVEL = logging.INFO

LOG_FIELDS = ["asctime", "levelname", "name", "message"]


def get_logger(name: str, log_file: str | None = None) -> logging.Logger:
    """Create and configure a logger.

    Args:
        name: The name of the logger.
        log_file: The file to log to. If None, file logging is disabled.

    Returns:
        Configured logger instance.

    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if logger.handlers:
        return logger

    console_formatter = logging.Formatter(
        " - ".join(f"%({field})s" for field in LOG_FIELDS),
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    if log_file:
        json_formatter = JsonFormatter(LOG_FIELDS)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(json_formatter)
        logger.addHandler(file_handler)

    return logger
