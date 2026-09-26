import logging
from assertpy import assert_that

from markov_solver.utils.logutils import ConsoleHandler, get_logger, set_log_level


class TestLogUtils:
    def test_get_logger(self) -> None:
        logger = get_logger("test_logger")
        assert_that(logger).is_not_none()
        assert_that(logger.name).is_equal_to("test_logger")

    def test_set_log_level(self) -> None:
        logger = get_logger("test_level_logger")
        set_log_level(logger, "DEBUG")
        assert_that(logger.level).is_equal_to(logging.DEBUG)

    def test_set_log_level_debug_emits_debug_records(self, capsys) -> None:  # type: ignore[no-untyped-def]
        logger = get_logger("test_debug_logger")
        handler = ConsoleHandler(logging.INFO)
        logger.addHandler(handler)
        logger.propagate = False
        set_log_level(logger, "DEBUG")
        logger.debug("Debug record")
        captured = capsys.readouterr()
        assert_that(handler.level).is_equal_to(logging.DEBUG)
        assert_that(captured.out).contains("Debug record")

    def test_set_log_level_info_drops_debug_records(self, capsys) -> None:  # type: ignore[no-untyped-def]
        logger = get_logger("test_info_logger")
        logger.addHandler(ConsoleHandler(logging.NOTSET))
        logger.propagate = False
        set_log_level(logger, "INFO")
        logger.debug("Debug record")
        captured = capsys.readouterr()
        assert_that(captured.out).does_not_contain("Debug record")

    def test_console_handler_init(self) -> None:
        handler = ConsoleHandler(logging.INFO)
        assert_that(handler.level).is_equal_to(logging.INFO)

    def test_console_handler_emit_info(self, capsys) -> None:  # type: ignore[no-untyped-def]
        handler = ConsoleHandler(logging.INFO)
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        handler.emit(record)
        captured = capsys.readouterr()
        assert_that(captured.out).contains("Test message")

    def test_console_handler_emit_error(self, capsys) -> None:  # type: ignore[no-untyped-def]
        handler = ConsoleHandler(logging.INFO)
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="Error message",
            args=(),
            exc_info=None,
        )
        handler.emit(record)
        captured = capsys.readouterr()
        assert_that(captured.err).contains("Error message")

    def test_console_handler_flush(self) -> None:
        handler = ConsoleHandler(logging.INFO)
        handler.flush()  # Should not raise
