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


def test_solve_command_with_args(runner, resource_path_root, tmp_path):
    definition_file = resource_path_root.joinpath(
        "definitions/simple/simple.definition.yaml"
    )
    with open(
        str(resource_path_root.joinpath("definitions/simple/expected-solution.txt")),
        "r",
    ) as file:
        expected_solution = file.read()

    outdir = tmp_path / "output"
    result = runner.invoke(
        main, ["solve", "--definition", str(definition_file), "--outdir", str(outdir)]
    )
    assert_that(result.exit_code).is_equal_to(0)
    assert_that(result.output).matches(r"Rainy.+0\.166666666666667")
    assert_that(result.output).matches(r"Sunny.+0\.833333333333333")


if __name__ == "__main__":
    pytest.main()
