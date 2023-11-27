import logging
from logging import Formatter, Handler, Logger, StreamHandler
from logging.handlers import RotatingFileHandler
import os
from typing import Optional

LOGGER = logging.getLogger(__name__)
LOG_FORMAT = "%(levelname)s [%(asctime)s] %(name)s <%(filename)s:%(lineno)d> %(message)s"


def _rotator(source: str, dest: str) -> None:
    os.replace(source, dest)
    # upload_name = f"{'.',join(source.split('/')[-1].split('.')[:-1])}_{int(time.time())}.log"
    # aws.upload_file(f"s3://bucket/path/logs/{upload_name}", dest)


def rotating_file_handler(filepath: str, max_bytes: int = 1073741824, backup_count: int = 1):
    rh = RotatingFileHandler(filepath, maxBytes=max_bytes, backupCount=backup_count)
    rh.rotator = _rotator
    return rh


def enable(
    filepath: str,
    log_to_console: bool = False,
    log_name: str = "lilypad",
    level: int | str = logging.INFO,
) -> Logger:
    def _add_handler(handler: Handler, formatter: Optional[Formatter] = None) -> None:
        if formatter is not None:
            handler.setFormatter(formatter)
        handler.setLevel(level)
        logger.addHandler(handler)

    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    LOGGER.info(f"Enabling logging, level: {logging.getLevelName(level)}")
    if log_to_console:
        _add_handler(StreamHandler(), Formatter(LOG_FORMAT))
    f = filepath if os.path.isabs(filepath) else os.path.join(os.getcwd(), "logs", filepath)
    _add_handler(rotating_file_handler(f), Formatter(LOG_FORMAT))
    return logger
