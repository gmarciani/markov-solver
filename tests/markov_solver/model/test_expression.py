# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Tests for transition value expressions."""

import pytest
from assertpy import assert_that

from markov_solver.model.expression import (
    ExpressionError,
    Token,
    substitute_symbols,
    tokenize,
)


class TestTokenize:
    @pytest.mark.parametrize(
        "expression, expected",
        [
            ("0.5", [Token("number", "0.5")]),
            ("1e-1", [Token("number", "1e-1")]),
            (".5E+3", [Token("number", ".5E+3")]),
            ("lambda", [Token("name", "lambda")]),
            ("mu_1", [Token("name", "mu_1")]),
            (
                " 3 * mu ",
                [Token("number", "3"), Token("operator", "*"), Token("name", "mu")],
            ),
            (
                "(1-p)**2/q",
                [
                    Token("operator", "("),
                    Token("number", "1"),
                    Token("operator", "-"),
                    Token("name", "p"),
                    Token("operator", ")"),
                    Token("operator", "**"),
                    Token("number", "2"),
                    Token("operator", "/"),
                    Token("name", "q"),
                ],
            ),
        ],
    )
    def test_tokenize(self, expression: str, expected: list[Token]) -> None:
        assert_that(list(tokenize(expression))).is_equal_to(expected)

    @pytest.mark.parametrize("expression", ["0.5;", "a.b", "x = 1", "'x'", "mu@2"])
    def test_tokenize_rejects_unexpected_characters(self, expression: str) -> None:
        assert_that(list).raises(ExpressionError).when_called_with(
            tokenize(expression)
        ).contains("unexpected character")


class TestSubstituteSymbols:
    @pytest.mark.parametrize(
        "expression, symbols, expected",
        [
            ("mu", {"mu": 2.0}, "(2.0)"),
            ("mu2", {"mu": 2.0, "mu2": 3.0}, "(3.0)"),
            ("1e-1", {"e": 2.718}, "1e-1"),
            ("lambda", {"a": 0.5, "lambda": 2.0}, "(2.0)"),
            ("3*mu", {"mu": 2.0}, "3*(2.0)"),
            ("(1-p)*0.25", {"p": 0.9}, "(1-(0.9))*0.25"),
            ("0.5", {}, "0.5"),
        ],
    )
    def test_substitute_symbols(
        self, expression: str, symbols: dict[str, float], expected: str
    ) -> None:
        assert_that(substitute_symbols(expression, symbols)).is_equal_to(expected)

    def test_substitute_symbols_undefined_symbol(self) -> None:
        assert_that(substitute_symbols).raises(ExpressionError).when_called_with(
            "3*mu", {"lambda": 1.0}
        ).contains("undefined symbol 'mu'")
