# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Arithmetic expressions used as transition values."""

import re
from typing import Iterator, Mapping, NamedTuple


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


def substitute_symbols(expression: str, symbols: Mapping[str, float]) -> str:
    """
    Replace every symbol name in the expression with its numeric value.
    Names are matched as whole tokens, so a symbol is never replaced inside a
    longer name or inside a numeric literal such as ``1e-1``.
    :param expression: the expression text.
    :param symbols: the symbol values, keyed by name.
    :return: the expression with the symbols replaced by their values.
    :raises ExpressionError: if the expression references an undefined symbol.
    """
    parts = []
    for token in tokenize(expression):
        if token.kind == "name":
            if token.text not in symbols:
                raise ExpressionError(
                    f"Invalid expression '{expression}': "
                    f"undefined symbol '{token.text}'"
                )
            parts.append(f"({symbols[token.text]!r})")
        else:
            parts.append(token.text)
    return "".join(parts)
