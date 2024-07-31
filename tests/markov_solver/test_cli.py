import pytest  # type: ignore

from assertpy import assert_that  # type: ignore
from click.testing import CliRunner
from markov_solver.cli import main


@pytest.fixture
def runner():
    return CliRunner()


def test_main_help(runner):
    result = runner.invoke(main, ["--help"])
    assert_that(result.exit_code).is_equal_to(0)
    assert_that(result.output).contains("Usage: ")


def test_main_version(runner):
    result = runner.invoke(main, ["--version"])
    assert_that(result.exit_code).is_equal_to(0)
    assert_that(result.output).contains("version 1.0.2")


def test_solve_command_no_args(runner):
    result = runner.invoke(main, ["solve"])
    assert_that(result.exit_code).is_equal_to(2)
    assert "Error: Missing option '--definition'" in result.output


@pytest.mark.parametrize(
    "definition_file, expected_exit_code, expected_probabilities",
    [
        (
                "definitions/simple/simple.definition.yaml",
                0,
                [
                    r"Rainy.+0\.166666666666667",
                    r"Sunny.+0\.833333333333333"
                ]
        ),
        (
                "definitions/symbolic/symbolic.definition.yaml",
                0,
                [
                    r"0.+0\.475836431226766",
                    r"1.+0\.356877323420074",
                    r"2.+0\.133828996282528",
                    r"3.+0\.0334572490706320"
                ]
        ),
    ],
)
def test_solve_command_with_args(runner, resource_path_root, tmp_path, definition_file, expected_exit_code, expected_probabilities):
    definition_file_path = resource_path_root.joinpath(definition_file)
    outdir = tmp_path / "output"

    result = runner.invoke(main, ["solve", "--definition", str(definition_file_path), "--outdir", str(outdir)])

    assert_that(result.exit_code).is_equal_to(expected_exit_code)
    for expected_probability in expected_probabilities:
        assert_that(result.output).matches(expected_probability)


if __name__ == "__main__":
    pytest.main()
