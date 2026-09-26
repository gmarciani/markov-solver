# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Arithmetic expressions used as transition values.

Transition values are numeric literals or arithmetic expressions over declared
symbols, using ``+``, ``-``, ``*``, ``/``, ``**`` and parentheses. They are
parsed by a small recursive-descent parser into sympy expressions: no Python
code is ever evaluated, so a definition file cannot execute arbitrary code.
"""

import re
from typing import Any, Iterator, List, Mapping, NamedTuple, Optional

import sympy  # type: ignore


class ExpressionError(ValueError):
    """Raised when a transition value expression is invalid."""


class Token(NamedTuple):
    kind: str  # "number", "name", "operator"
    text: str


_TOKEN_PATTERN = re.compile(
    r"\s*(?:"
    r"(?P<number>(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?)"
    r"|(?P<name>[A-Za-z_]\w*)"
    r"|(?P<operator>\*\*|[-+*/()])"
    r")"
)


def tokenize(expression: str) -> Iterator[Token]:
    """
    Split an arithmetic expression into number, name and operator tokens.
    :param expression: the expression text.
    :return: the tokens, in order.
    :raises ExpressionError: on any character that is not part of a valid token.
    """
    position = 0
    end = len(expression)
    while position < end:
        if expression[position:].isspace():
            return
        match = _TOKEN_PATTERN.match(expression, position)
        if match is None:
            raise ExpressionError(
                f"Invalid expression '{expression}': "
                f"unexpected character '{expression[position]}' at position {position}"
            )
        kind = str(match.lastgroup)
        yield Token(kind, match.group(kind))
        position = match.end()


class _Parser:
    """
    Recursive-descent parser for the grammar::

        expr   := term (("+" | "-") term)*
        term   := unary (("*" | "/") unary)*
        unary  := ("+" | "-") unary | power
        power  := atom ("**" unary)?
        atom   := NUMBER | NAME | "(" expr ")"
    """

    def __init__(self, expression: str) -> None:
        self.expression = expression
        self.tokens: List[Token] = list(tokenize(expression))
        self.position = 0

    def parse(self) -> Any:
        if not self.tokens:
            raise self._error("empty expression")
        result = self._expr()
        if self.position < len(self.tokens):
            raise self._error(f"unexpected '{self.tokens[self.position].text}'")
        return result

    def _peek(self) -> Optional[Token]:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def _accept(self, *operators: str) -> Optional[str]:
        token = self._peek()
        if token is not None and token.kind == "operator" and token.text in operators:
            self.position += 1
            return token.text
        return None

    def _error(self, reason: str) -> ExpressionError:
        return ExpressionError(f"Invalid expression '{self.expression}': {reason}")

    def _expr(self) -> Any:
        result = self._term()
        while (operator := self._accept("+", "-")) is not None:
            operand = self._term()
            result = result + operand if operator == "+" else result - operand
        return result

    def _term(self) -> Any:
        result = self._unary()
        while (operator := self._accept("*", "/")) is not None:
            operand = self._unary()
            result = result * operand if operator == "*" else result / operand
        return result

    def _unary(self) -> Any:
        operator = self._accept("+", "-")
        if operator is None:
            return self._power()
        operand = self._unary()
        return operand if operator == "+" else -operand

    def _power(self) -> Any:
        base = self._atom()
        if self._accept("**") is not None:
            return base ** self._unary()
        return base

    def _atom(self) -> Any:
        token = self._peek()
        if token is None:
            raise self._error("unexpected end of expression")
        self.position += 1
        if token.kind == "number":
            return (
                sympy.Float(token.text)
                if _is_decimal(token.text)
                else sympy.Integer(token.text)
            )
        if token.kind == "name":
            return sympy.Symbol(token.text)
        if token.text == "(":
            result = self._expr()
            if self._accept(")") is None:
                raise self._error("missing closing parenthesis")
            return result
        raise self._error(f"unexpected '{token.text}'")


def _is_decimal(literal: str) -> bool:
    return any(c in literal for c in ".eE")


def parse_expression(expression: str) -> Any:
    """
    Parse an arithmetic expression into a sympy expression.
    Names become sympy symbols; nothing is executed.
    :param expression: the expression text.
    :return: the sympy expression.
    :raises ExpressionError: if the expression is not valid arithmetic.
    """
    return _Parser(expression).parse()


def evaluate_expression(expression: str, symbols: Mapping[str, float]) -> float:
    """
    Evaluate an arithmetic expression, substituting the given symbol values.
    :param expression: the expression text.
    :param symbols: the symbol values, keyed by name.
    :return: the numeric value of the expression.
    :raises ExpressionError: if the expression is invalid, references an
        undefined symbol, or has no finite value (e.g. division by zero).
    """
    parsed = parse_expression(expression)
    undefined = sorted(s.name for s in parsed.free_symbols if s.name not in symbols)
    if undefined:
        names = ", ".join(f"'{name}'" for name in undefined)
        raise ExpressionError(
            f"Invalid expression '{expression}': undefined symbol{'s'[:len(undefined) > 1]} {names}"
        )
    value = parsed.subs({sympy.Symbol(k): sympy.Float(v) for k, v in symbols.items()})
    if not value.is_finite:
        raise ExpressionError(
            f"Invalid expression '{expression}': value is not finite (division by zero?)"
        )
    return float(value)
