# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Tests for the installed package metadata and the supported Python versions.

The supported range is declared once, in ``SUPPORTED_PYTHON_VERSIONS`` below,
and the default interpreter in ``DEFAULT_PYTHON_VERSION``. These tests fail
when the metadata, tox, CI workflows or README badge drift from them.
"""

import re
import tomllib
from importlib.metadata import metadata
from pathlib import Path
from typing import Any

import pytest
import yaml
from assertpy import assert_that

REPO_ROOT = Path(__file__).parents[2]

SUPPORTED_PYTHON_VERSIONS = ["3.12", "3.13", "3.14"]
DEFAULT_PYTHON_VERSION = "3.14"


def tox_env_name(version: str) -> str:
    """Return the tox environment name for a Python version, e.g. ``py312``."""
    return "py" + version.replace(".", "")


def load_workflow(name: str) -> dict[str, Any]:
    """Load a GitHub Actions workflow from the repository."""
    path = REPO_ROOT / ".github" / "workflows" / name
    workflow: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8"))
    return workflow


def load_pyproject() -> dict[str, Any]:
    """Load ``pyproject.toml`` from the repository."""
    return tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_package_summary_describes_markov_solver() -> None:
    summary = metadata("markov-solver")["Summary"]
    assert_that(summary).contains("Markov chains")
    assert_that(summary).does_not_contain("OpenAPI")


def test_default_python_version_is_supported() -> None:
    assert_that(SUPPORTED_PYTHON_VERSIONS).contains(DEFAULT_PYTHON_VERSION)


def test_package_requires_the_oldest_supported_version() -> None:
    requires_python = metadata("markov-solver")["Requires-Python"]
    assert_that(requires_python).is_equal_to(f">={SUPPORTED_PYTHON_VERSIONS[0]}")


def test_package_classifiers_list_exactly_the_supported_versions() -> None:
    classifiers = metadata("markov-solver").get_all("Classifier") or []
    versions = [
        c.removeprefix("Programming Language :: Python :: ")
        for c in classifiers
        if re.fullmatch(r"Programming Language :: Python :: 3\.\d+", c)
    ]
    assert_that(versions).is_equal_to(SUPPORTED_PYTHON_VERSIONS)


def test_black_targets_every_supported_version() -> None:
    target_version = load_pyproject()["tool"]["black"]["target-version"]
    expected = [tox_env_name(v) for v in SUPPORTED_PYTHON_VERSIONS]
    assert_that(target_version).is_equal_to(expected)


def test_mypy_checks_the_default_version() -> None:
    python_version = load_pyproject()["tool"]["mypy"]["python_version"]
    assert_that(python_version).is_equal_to(DEFAULT_PYTHON_VERSION)


def test_tox_envlist_covers_supported_versions() -> None:
    tox_ini = (REPO_ROOT / "tox.ini").read_text(encoding="utf-8")
    match = re.search(r"^envlist = (.+)$", tox_ini, re.M)
    assert match is not None
    envs = match.group(1).split(",")
    expected = [tox_env_name(v) for v in SUPPORTED_PYTHON_VERSIONS]
    assert_that(envs[: len(expected)]).is_equal_to(expected)


def test_tox_defaults_to_the_default_version() -> None:
    tox_ini = (REPO_ROOT / "tox.ini").read_text(encoding="utf-8")
    match = re.search(r"^default_base_python = (.+)$", tox_ini, re.M)
    assert match is not None
    assert_that(match.group(1).strip()).is_equal_to(
        tox_env_name(DEFAULT_PYTHON_VERSION)
    )


@pytest.mark.parametrize("workflow", ["pr-validation.yaml", "test.yaml"])
def test_ci_runs_unit_tests_on_every_supported_version(workflow: str) -> None:
    matrix = load_workflow(workflow)["jobs"]["test"]["strategy"]["matrix"]
    versions = [str(v) for v in matrix["python-version"]]
    assert_that(versions).is_equal_to(SUPPORTED_PYTHON_VERSIONS)


@pytest.mark.parametrize(
    "workflow, job",
    [
        ("pr-validation.yaml", "quality"),
        ("test.yaml", "quality"),
        ("docs.yaml", "build"),
        ("release.yaml", "publish"),
    ],
)
def test_single_version_ci_jobs_use_the_default_version(
    workflow: str, job: str
) -> None:
    steps = load_workflow(workflow)["jobs"][job]["steps"]
    setup = next(s for s in steps if "setup-python" in s.get("uses", ""))
    assert_that(str(setup["with"]["python-version"])).is_equal_to(
        DEFAULT_PYTHON_VERSION
    )


def test_makefile_pins_a_release_of_the_default_version() -> None:
    makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    match = re.search(r"^PYTHON_VERSION = (.+)$", makefile, re.M)
    assert match is not None
    assert_that(match.group(1).strip()).starts_with(f"{DEFAULT_PYTHON_VERSION}.")


def test_readme_badge_lists_supported_versions() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    match = re.search(r"img\.shields\.io/badge/python-([^-]+)-blue\.svg", readme)
    assert match is not None
    assert_that(match.group(1).split("%20%7C%20")).is_equal_to(
        SUPPORTED_PYTHON_VERSIONS
    )
