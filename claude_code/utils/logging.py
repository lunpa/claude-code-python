"""Logging utilities"""
import logging
import sys
from pathlib import Path


def setup_logging(debug: bool = False, log_file: Path = None) -> None:
    """Setup logging configuration"""
    level = logging.DEBUG if debug else logging.INFO

    handlers = [logging.StreamHandler(sys.stdout)]

    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger"""
    return logging.getLogger(name)