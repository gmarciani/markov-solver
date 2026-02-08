# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Tests for TransitionMatrixParser."""

import pytest

from markov_solver.core.parser.transition_matrix_parser import TransitionMatrixParser
from markov_solver.core.parser.base import ParserError


class TestTransitionMatrixParser:
    """Tests for TransitionMatrixParser."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.parser = TransitionMatrixParser()

    def test_parse_simple_matrix(self) -> None:
        """Test parsing a simple transition matrix."""
        content = """
states:
  - S0
  - S1
  - S2
transitions:
  S0:
    S0: 0.5
    S1: 0.5
  S1:
    S2: 1.0
  S2:
    S2: 1.0
"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 3
        assert len(mc.links) == 4

    def test_parse_json_format(self) -> None:
        """Test parsing JSON format."""
        content = """{
    "states": ["A", "B"],
    "transitions": {
        "A": {"B": 1.0},
        "B": {"A": 0.5, "B": 0.5}
    }
}"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 2
        assert len(mc.links) == 3

    def test_parse_with_symbols(self) -> None:
        """Test parsing with symbols."""
        content = """
states:
  - S0
  - S1
symbols:
  lambda: 1.5
  mu: 2.0
transitions:
  S0:
    S1: lambda
  S1:
    S0: mu
"""
        mc = self.parser.parse(content)

        assert len(mc.symbols) == 2
        assert mc.symbols["lambda"] == 1.5
        assert mc.symbols["mu"] == 2.0

    def test_parse_with_initial_state(self) -> None:
        """Test parsing with initial state specified."""
        content = """
states:
  - S0
  - S1
initial: S0
transitions:
  S0:
    S1: 1.0
"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 2

    def test_parse_invalid_yaml(self) -> None:
        """Test parsing invalid YAML raises ParserError."""
        content = "states: [invalid"
        with pytest.raises(ParserError, match="Invalid YAML/JSON"):
            self.parser.parse(content)

    def test_parse_empty_content(self) -> None:
        """Test parsing empty content raises ParserError."""
        with pytest.raises(ParserError, match="Empty definition file"):
            self.parser.parse("")

    def test_parse_null_content(self) -> None:
        """Test parsing null YAML raises ParserError."""
        with pytest.raises(ParserError, match="Empty definition file"):
            self.parser.parse("null")

    def test_parse_missing_states(self) -> None:
        """Test parsing without states field raises ParserError."""
        content = """
transitions:
  S0:
    S1: 1.0
"""
        with pytest.raises(ParserError, match="Invalid transition matrix"):
            self.parser.parse(content)

    def test_parse_missing_transitions(self) -> None:
        """Test parsing without transitions field raises ParserError."""
        content = """
states:
  - S0
  - S1
"""
        with pytest.raises(ParserError, match="Invalid transition matrix"):
            self.parser.parse(content)

    def test_parse_empty_states(self) -> None:
        """Test parsing with empty states list raises ParserError."""
        content = """
states: []
transitions: {}
"""
        # Empty states is technically valid per schema
        mc = self.parser.parse(content)
        assert len(mc.states) == 0

    def test_parse_string_transition_values(self) -> None:
        """Test parsing with string transition values (symbolic)."""
        content = """
states:
  - A
  - B
transitions:
  A:
    B: "lambda"
  B:
    A: "mu"
"""
        mc = self.parser.parse(content)

        links = list(mc.links)
        values = {link.value for link in links}
        assert "lambda" in values
        assert "mu" in values

    def test_parse_float_transition_values(self) -> None:
        """Test parsing with float transition values."""
        content = """
states:
  - A
  - B
transitions:
  A:
    B: 0.75
  B:
    A: 0.25
"""
        mc = self.parser.parse(content)

        links = list(mc.links)
        values = {link.value for link in links}
        assert "0.75" in values
        assert "0.25" in values

    def test_supports_extension_always_false(self) -> None:
        """Test supports_extension always returns False (explicit use only)."""
        assert self.parser.supports_extension(".yaml") is False
        assert self.parser.supports_extension(".yml") is False
        assert self.parser.supports_extension(".json") is False
        assert self.parser.supports_extension(".csv") is False
        assert self.parser.supports_extension(".dot") is False

    def test_parse_symbols_with_int_values(self) -> None:
        """Test parsing symbols with integer values."""
        content = """
states:
  - A
  - B
symbols:
  rate: 5
transitions:
  A:
    B: rate
"""
        mc = self.parser.parse(content)

        assert mc.symbols["rate"] == 5.0

    def test_parse_symbols_with_string_values(self) -> None:
        """Test parsing symbols with string numeric values."""
        content = """
states:
  - A
  - B
symbols:
  rate: "3.14"
transitions:
  A:
    B: rate
"""
        mc = self.parser.parse(content)

        assert mc.symbols["rate"] == 3.14

    def test_parse_single_state_self_loop(self) -> None:
        """Test parsing single state with self-loop."""
        content = """
states:
  - A
transitions:
  A:
    A: 1.0
"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 1
        assert len(mc.links) == 1
