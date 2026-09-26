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
    assert_that(result.output).contains("version 2.1.0")


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
            [r"Rainy.+0\.166666666666667", r"Sunny.+0\.833333333333333"],
        ),
        (
            "definitions/simple/simple.matrix.yaml",
            0,
            [r"Rainy.+0\.166666666666667", r"Sunny.+0\.833333333333333"],
        ),
        (
            "definitions/symbolic/symbolic.definition.yaml",
            0,
            [
                r"0.+0\.475836431226766",
                r"1.+0\.356877323420074",
                r"2.+0\.133828996282528",
                r"3.+0\.0334572490706320",
            ],
        ),
    ],
)
def test_solve_command_with_args(
    runner,
    resource_path_root,
    tmp_path,
    definition_file,
    expected_exit_code,
    expected_probabilities,
):
    definition_file_path = resource_path_root.joinpath(definition_file)
    outdir = tmp_path / "output"

    result = runner.invoke(
        main,
        ["solve", "--definition", str(definition_file_path), "--outdir", str(outdir)],
    )

    assert_that(result.exit_code).is_equal_to(expected_exit_code)
    for expected_probability in expected_probabilities:
        assert_that(result.output).matches(expected_probability)


@pytest.mark.parametrize(
    "debug_flag, debug_message_expected", [("--debug", True), ("--no-debug", False)]
)
def test_debug_flag_controls_debug_logging(
    runner, resource_path_root, tmp_path, caplog, debug_flag, debug_message_expected
):
    definition_file_path = resource_path_root.joinpath(
        "definitions/simple/simple.definition.yaml"
    )

    result = runner.invoke(
        main,
        [
            debug_flag,
            "solve",
            "--definition",
            str(definition_file_path),
            "--outdir",
            str(tmp_path),
        ],
    )

    assert_that(result.exit_code).is_equal_to(0)
    debug_messages = [r.message for r in caplog.records if r.levelname == "DEBUG"]
    if debug_message_expected:
        assert_that(debug_messages).contains("Debug Mode: on")
    else:
        assert_that(debug_messages).is_empty()


@pytest.mark.parametrize(
    "filename, content, expected_error",
    [
        ("chain.md", "# not a definition", "Unsupported file extension: .md"),
        ("chain.yaml", "chain: [{from: A}]", "Invalid chain definition"),
        ("chain.yaml", "chain: [", "Invalid YAML/JSON"),
    ],
)
def test_solve_command_invalid_definition_reports_error_without_traceback(
    runner, tmp_path, filename, content, expected_error
):
    definition_file_path = tmp_path / filename
    definition_file_path.write_text(content)

    result = runner.invoke(
        main,
        ["solve", "--definition", str(definition_file_path), "--outdir", str(tmp_path)],
    )

    assert_that(result.exit_code).is_equal_to(1)
    assert_that(result.exception).is_instance_of(SystemExit)
    assert_that(result.output).contains("Error: Invalid definition", expected_error)
    assert_that(result.output).does_not_contain("Traceback")


if __name__ == "__main__":
    pytest.main()
