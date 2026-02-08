from assertpy import assert_that

from markov_solver.utils.file_utils import (
    append_csv,
    append_list_of_numbers,
    append_list_of_pairs,
    create_dir_tree,
    empty_file,
    exists_file,
    is_empty_file,
    save_csv,
    save_header_csv,
    save_list_of_numbers,
    save_list_of_pairs,
    save_txt,
)


class TestFileUtils:
    def test_exists_file_true(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        assert_that(exists_file(str(test_file))).is_true()

    def test_exists_file_false(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "nonexistent.txt"
        assert_that(exists_file(str(test_file))).is_false()

    def test_is_empty_file_true(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "empty.txt"
        test_file.write_text("")
        assert_that(is_empty_file(str(test_file))).is_true()

    def test_is_empty_file_false(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "nonempty.txt"
        test_file.write_text("content")
        assert_that(is_empty_file(str(test_file))).is_false()

    def test_empty_file(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        empty_file(str(test_file))
        assert_that(is_empty_file(str(test_file))).is_true()

    def test_create_dir_tree(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        nested_file = tmp_path / "a" / "b" / "c" / "test.txt"
        create_dir_tree(str(nested_file))
        assert_that((tmp_path / "a" / "b" / "c").exists()).is_true()

    def test_save_list_of_numbers(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "numbers.txt"
        save_list_of_numbers(str(test_file), [1, 2, 3.5])
        content = test_file.read_text()
        assert_that(content).is_equal_to("1\n2\n3.5\n")

    def test_append_list_of_numbers(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "numbers.txt"
        save_list_of_numbers(str(test_file), [1])
        append_list_of_numbers(str(test_file), [2, 3])
        content = test_file.read_text()
        assert_that(content).is_equal_to("1\n2\n3\n")

    def test_save_list_of_pairs(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "pairs.txt"
        save_list_of_pairs(str(test_file), [(1, 2), (3, 4)])
        content = test_file.read_text()
        assert_that(content).is_equal_to("1,2\n3,4\n")

    def test_append_list_of_pairs(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "pairs.txt"
        save_list_of_pairs(str(test_file), [(1, 2)])
        append_list_of_pairs(str(test_file), [(3, 4)])
        content = test_file.read_text()
        assert_that(content).is_equal_to("1,2\n3,4\n")

    def test_save_csv(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "test.csv"
        save_csv(str(test_file), {"name": "John", "age": "30"})
        content = test_file.read_text()
        assert_that(content).contains("name,age")
        assert_that(content).contains("John,30")

    def test_save_header_csv(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "test.csv"
        save_header_csv(str(test_file), {"name": "John", "age": "30"})
        content = test_file.read_text()
        assert_that(content).is_equal_to("name,age\n")

    def test_append_csv(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "test.csv"
        test_file.write_text("name,age\n")
        append_csv(str(test_file), {"name": "John", "age": "30"})
        content = test_file.read_text()
        assert_that(content).is_equal_to("name,age\nJohn,30\n")

    def test_save_txt(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "test.txt"
        save_txt("Hello World", str(test_file))
        content = test_file.read_text()
        assert_that(content).is_equal_to("Hello World")

    def test_save_txt_append(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "test.txt"
        save_txt("Hello", str(test_file))
        save_txt(" World", str(test_file), append=True)
        content = test_file.read_text()
        assert_that(content).is_equal_to("Hello World")

    def test_save_txt_empty(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "test.txt"
        test_file.write_text("Old content")
        save_txt("New content", str(test_file), empty=True)
        content = test_file.read_text()
        assert_that(content).is_equal_to("New content")
