"""
Utilities for logging.
"""

import logging
import sys

FORMATTER = logging.Formatter("%(asctime)-15s [%(levelname)s] %(message)s")
LEVEL = logging.INFO


class ConsoleHandler(logging.StreamHandler):  # type: ignore[type-arg]
    """
    A handler that logs to console in the sensible way.
    StreamHandler can log to *one of* sys.stdout or sys.stderr.
    It is more sensible to log to sys.stdout by default with only error
    (logging.ERROR and above) messages going to sys.stderr. This is how
    ConsoleHandler behaves.
    """

    def __init__(self, level: int, formatter: logging.Formatter = FORMATTER) -> None:
        logging.StreamHandler.__init__(self)
        self.stream = None  # reset it; we are not going to use it anyway
        self.setLevel(level)
        self.setFormatter(formatter)

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno >= logging.ERROR:
            self.__emit(record, sys.stderr)
        else:
            self.__emit(record, sys.stdout)

    def __emit(self, record: logging.LogRecord, strm: object) -> None:
        self.stream = strm  # type: ignore[assignment]
        logging.StreamHandler.emit(self, record)

    def flush(self) -> None:
        # Workaround a bug in logging module
        # See:
        #   http://bugs.python.org/issue6333
        if self.stream and hasattr(self.stream, "flush") and not self.stream.closed:  # type: ignore[union-attr]
            logging.StreamHandler.flush(self)


def get_logger(name: str) -> logging.Logger:
    """
    Configure the logger.
    :param name: the logger name.
    :return: the logger.
    """
    # The handler accepts every record (NOTSET) so that the effective level is
    # decided by the loggers alone; otherwise set_log_level could never lower
    # the verbosity below the handler threshold.
    logging.basicConfig(
        level=LEVEL, handlers=[ConsoleHandler(logging.NOTSET, FORMATTER)]
    )
    return logging.getLogger(name)


def set_log_level(logger: logging.Logger, level: str) -> None:
    """
    Set the level of the logger and of any handler attached to it or to the
    root logger that would otherwise filter out records at the new level.
    :param logger: the logger.
    :param level: the level name, e.g. "DEBUG".
    """
    logger.setLevel(level)
    numeric_level = logging.getLevelName(level)
    for handler in logger.handlers + logging.getLogger().handlers:
        if handler.level > numeric_level:
            handler.setLevel(numeric_level)
