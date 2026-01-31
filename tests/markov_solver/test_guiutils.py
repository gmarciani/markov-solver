from assertpy import assert_that

from markov_solver.utils.guiutils import get_splash, print_progress


class TestGuiUtils:
    def test_get_splash(self) -> None:
        result = get_splash("Test")
        assert_that(result).is_not_empty()

    def test_print_progress(self, capsys) -> None:  # type: ignore[no-untyped-def]
        print_progress(50, 100)
        captured = capsys.readouterr()
        assert_that(captured.out).contains("50%")
        assert_that(captured.out).contains("PROGRESS")

    def test_print_progress_with_message(self, capsys) -> None:  # type: ignore[no-untyped-def]
        print_progress(50, 100, message="Processing")
        captured = capsys.readouterr()
        assert_that(captured.out).contains("Processing")

    def test_print_progress_custom_prefix(self, capsys) -> None:  # type: ignore[no-untyped-def]
        print_progress(50, 100, prefix="LOADING")
        captured = capsys.readouterr()
        assert_that(captured.out).contains("LOADING")

    def test_print_progress_custom_suffix(self, capsys) -> None:  # type: ignore[no-untyped-def]
        print_progress(50, 100, suffix="Done")
        captured = capsys.readouterr()
        assert_that(captured.out).contains("Done")

    def test_print_progress_decimals(self, capsys) -> None:  # type: ignore[no-untyped-def]
        print_progress(33, 100, decimals=2)
        captured = capsys.readouterr()
        assert_that(captured.out).contains("33.00%")

    def test_print_progress_bar_length(self, capsys) -> None:  # type: ignore[no-untyped-def]
        print_progress(50, 100, bar_length=20)
        captured = capsys.readouterr()
        assert_that(captured.out).contains("=")
