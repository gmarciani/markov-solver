# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Tests for the installed package metadata."""

from importlib.metadata import metadata

from assertpy import assert_that


def test_package_summary_describes_markov_solver() -> None:
    summary = metadata("markov-solver")["Summary"]
    assert_that(summary).contains("Markov chains")
    assert_that(summary).does_not_contain("OpenAPI")
