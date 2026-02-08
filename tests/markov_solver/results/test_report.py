from assertpy import assert_that

from markov_solver.results.report import SimpleReport


class TestSimpleReport:
    def test_init(self) -> None:
        report = SimpleReport("Test Report")
        assert_that(report.title).is_equal_to("Test Report")
        assert_that(report.params).is_empty()

    def test_add(self) -> None:
        report = SimpleReport("Test Report")
        report.add("section1", "param1", "value1")
        assert_that(report.params).contains_key("section1")
        assert_that(report.params["section1"]).contains(("param1", "value1"))

    def test_add_multiple_to_same_section(self) -> None:
        report = SimpleReport("Test Report")
        report.add("section1", "param1", "value1")
        report.add("section1", "param2", "value2")
        assert_that(len(report.params["section1"])).is_equal_to(2)

    def test_add_all(self) -> None:
        class TestObj:
            def __init__(self) -> None:
                self.name = "test"
                self.value = 3.14159
                self._private = "hidden"

        report = SimpleReport("Test Report")
        report.add_all("section1", TestObj())
        assert_that(report.get("section1", "name")).is_equal_to("test")
        assert_that(report.get("section1", "value")).is_close_to(3.14159, 0.001)

    def test_add_all_attrs(self) -> None:
        class TestObj:
            def __init__(self) -> None:
                self.name = "test"
                self.value = 3.14159
                self.other = "ignored"

        report = SimpleReport("Test Report")
        report.add_all_attrs("section1", TestObj(), "name", "value")
        assert_that(report.get("section1", "name")).is_equal_to("test")
        assert_that(report.get("section1", "value")).is_close_to(3.14159, 0.001)

    def test_add_all_attrs_with_float(self) -> None:
        class TestObj:
            def __init__(self) -> None:
                self.value = 3.14159265358979

        report = SimpleReport("Test Report")
        report.add_all_attrs("section1", TestObj(), "value")
        assert_that(report.get("section1", "value")).is_not_none()

    def test_get_existing(self) -> None:
        report = SimpleReport("Test Report")
        report.add("section1", "param1", "value1")
        assert_that(report.get("section1", "param1")).is_equal_to("value1")

    def test_get_non_existing(self) -> None:
        report = SimpleReport("Test Report")
        report.add("section1", "param1", "value1")
        assert_that(report.get("section1", "param2")).is_none()

    def test_save_txt(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        report = SimpleReport("Test Report")
        report.add("section1", "param1", "value1")
        test_file = tmp_path / "report.txt"
        report.save_txt(str(test_file))
        content = test_file.read_text()
        assert_that(content).contains("Test Report")
        assert_that(content).contains("param1")

    def test_save_txt_append(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        report = SimpleReport("Test Report")
        report.add("section1", "param1", "value1")
        test_file = tmp_path / "report.txt"
        report.save_txt(str(test_file))
        report.save_txt(str(test_file), append=True)
        content = test_file.read_text()
        assert_that(content.count("Test Report")).is_equal_to(2)

    def test_save_txt_empty(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        test_file = tmp_path / "report.txt"
        test_file.write_text("Old content")
        report = SimpleReport("Test Report")
        report.add("section1", "param1", "value1")
        report.save_txt(str(test_file), empty=True)
        content = test_file.read_text()
        assert_that(content).does_not_contain("Old content")

    def test_save_csv(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        report = SimpleReport("Test Report")
        report.add("section1", "param1", "value1")
        report.add("section1", "param2", 3.14)
        test_file = tmp_path / "report.csv"
        report.save_csv(str(test_file))
        content = test_file.read_text()
        assert_that(content).contains("name")
        assert_that(content).contains("Test Report")

    def test_str(self) -> None:
        report = SimpleReport("Test Report")
        report.add("section1", "param1", "value1")
        report.add("section1", "param2", 3.14)
        result = str(report)
        assert_that(result).contains("Test Report")
        assert_that(result).contains("section1")
        assert_that(result).contains("param1")
