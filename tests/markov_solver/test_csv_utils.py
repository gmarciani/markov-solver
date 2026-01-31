from assertpy import assert_that

from markov_solver.utils.csv_utils import read_csv, save_csv, str_csv


class TestCsvUtils:
    def test_save_csv(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "test.csv"
        save_csv(str(test_file), ["name", "age"], [("John", "30"), ("Jane", "25")])
        content = test_file.read_text()
        assert_that(content).contains("name,age")
        assert_that(content).contains("John,30")
        assert_that(content).contains("Jane,25")

    def test_save_csv_append(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "test.csv"
        save_csv(str(test_file), ["name", "age"], [("John", "30")])
        save_csv(str(test_file), ["name", "age"], [("Jane", "25")], append=True)
        content = test_file.read_text()
        assert_that(content).contains("John,30")
        assert_that(content).contains("Jane,25")

    def test_save_csv_skip_header(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "test.csv"
        test_file.write_text("name,age\n")
        save_csv(
            str(test_file),
            ["name", "age"],
            [("John", "30")],
            append=True,
            skip_header=True,
        )
        content = test_file.read_text()
        lines = content.strip().split("\n")
        assert_that(len(lines)).is_equal_to(2)

    def test_save_csv_empty(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "test.csv"
        test_file.write_text("old,data\nold,values\n")
        save_csv(str(test_file), ["name", "age"], [("John", "30")], empty=True)
        content = test_file.read_text()
        assert_that(content).does_not_contain("old")

    def test_str_csv(self) -> None:
        assert_that(str_csv("Hello World")).is_equal_to("hello_world")
        assert_that(str_csv("path/to/file")).is_equal_to("path_to_file")

    def test_read_csv(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "test.csv"
        test_file.write_text("name,age\nJohn,30\nJane,25\n")
        result = read_csv(str(test_file))
        assert_that(len(result)).is_equal_to(2)
        assert_that(result[0]["name"]).is_equal_to("John")
        assert_that(result[0]["age"]).is_equal_to("30")
        assert_that(result[1]["name"]).is_equal_to("Jane")
