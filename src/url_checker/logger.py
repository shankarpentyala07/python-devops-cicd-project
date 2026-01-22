"""Logging configuration module."""

import logging
import sys


def setup_logger(verbose: bool = False) -> logging.Logger:
    """
    Configure and return logger for URL checker.

    Args:
        verbose: Enable DEBUG level logging if True, otherwise use INFO level.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("url_checker")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Remove any existing handlers to avoid duplicate logs
    if logger.handlers:
        logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger
