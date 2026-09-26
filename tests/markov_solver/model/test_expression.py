# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Tests for transition value expressions."""

import pytest
from assertpy import assert_that

import sympy

from markov_solver.model.expression import (
    ExpressionError,
    Token,
    evaluate_expression,
    parse_expression,
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


class TestParseExpression:
    @pytest.mark.parametrize(
        "expression, expected",
        [
            ("0.5", sympy.Float("0.5")),
            ("2", sympy.Integer(2)),
            ("mu", sympy.Symbol("mu")),
            ("3*mu", 3 * sympy.Symbol("mu")),
            ("1-p", 1 - sympy.Symbol("p")),
            ("(1-p)*0.25", (1 - sympy.Symbol("p")) * sympy.Float("0.25")),
            ("-x", -sympy.Symbol("x")),
            ("--x", sympy.Symbol("x")),
            ("+x", sympy.Symbol("x")),
            # precedence: * binds tighter than +, ** tighter than unary minus
            ("1+2*x", 1 + 2 * sympy.Symbol("x")),
            ("-x**2", -(sympy.Symbol("x") ** 2)),
            ("2**-1", sympy.Rational(1, 2)),
            ("x**2**3", sympy.Symbol("x") ** 8),
            ("a/b/c", sympy.Symbol("a") / sympy.Symbol("b") / sympy.Symbol("c")),
            ("a-b-c", sympy.Symbol("a") - sympy.Symbol("b") - sympy.Symbol("c")),
            (" ( lambda ) ", sympy.Symbol("lambda")),
        ],
    )
    def test_parse_expression(self, expression: str, expected: sympy.Expr) -> None:
        assert_that(parse_expression(expression) - expected).is_equal_to(0)

    @pytest.mark.parametrize(
        "expression, reason",
        [
            ("", "empty expression"),
            ("   ", "empty expression"),
            ("1 +", "unexpected end of expression"),
            ("(1", "missing closing parenthesis"),
            ("1)", "unexpected ')'"),
            ("* 2", "unexpected '*'"),
            ("2 3", "unexpected '3'"),
            ("mu(2)", "unexpected '('"),
            ("1 ** ** 2", "unexpected '**'"),
        ],
    )
    def test_parse_expression_rejects_malformed_input(
        self, expression: str, reason: str
    ) -> None:
        assert_that(parse_expression).raises(ExpressionError).when_called_with(
            expression
        ).contains(reason)

    @pytest.mark.parametrize(
        "expression",
        [
            "print('x') or 0.5",
            "__import__('os').system('true')",
            "open('/etc/passwd')",
            "[0.5][0]",
            "{'a': 1}",
            "0.5 if True else 1",
            "x.real",
            "0.5; import os",
        ],
    )
    def test_parse_expression_never_evaluates_python(self, expression: str) -> None:
        assert_that(parse_expression).raises(ExpressionError).when_called_with(
            expression
        )


class TestEvaluateExpression:
    @pytest.mark.parametrize(
        "expression, symbols, expected",
        [
            ("0.5", {}, 0.5),
            ("1e-1", {"e": 2.718}, 0.1),
            ("mu", {"mu": 2.0}, 2.0),
            ("mu2", {"mu": 2.0, "mu2": 3.0}, 3.0),
            ("lambda", {"a": 0.5, "lambda": 2.0}, 2.0),
            ("3*mu", {"mu": 2.0}, 6.0),
            ("(1-p)*0.25", {"p": 0.9}, 0.025),
            ("lambda/(lambda+mu)", {"lambda": 1.0, "mu": 3.0}, 0.25),
            ("2**-1", {}, 0.5),
        ],
    )
    def test_evaluate_expression(
        self, expression: str, symbols: dict[str, float], expected: float
    ) -> None:
        assert_that(evaluate_expression(expression, symbols)).is_close_to(
            expected, 1e-12
        )

    def test_evaluate_expression_undefined_symbol(self) -> None:
        assert_that(evaluate_expression).raises(ExpressionError).when_called_with(
            "3*mu", {"lambda": 1.0}
        ).contains("undefined symbol 'mu'")

    def test_evaluate_expression_lists_all_undefined_symbols(self) -> None:
        assert_that(evaluate_expression).raises(ExpressionError).when_called_with(
            "a*b", {}
        ).contains("undefined symbols 'a', 'b'")

    def test_evaluate_expression_division_by_zero(self) -> None:
        assert_that(evaluate_expression).raises(ExpressionError).when_called_with(
            "1/(mu-mu)", {"mu": 2.0}
        ).contains("not finite")
