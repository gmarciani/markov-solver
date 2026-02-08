# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Tests for ChainFormatParser."""

import pytest

from markov_solver.core.parser.chain_format_parser import ChainFormatParser
from markov_solver.core.parser.base import ParserError


class TestChainFormatParser:
    """Tests for ChainFormatParser."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.parser = ChainFormatParser()

    def test_parse_simple_chain(self) -> None:
        """Test parsing a simple chain definition."""
        content = """
chain:
  - from: "S0"
    to: "S1"
    value: "0.5"
  - from: "S1"
    to: "S2"
    value: "1.0"
"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 3
        assert len(mc.links) == 2

    def test_parse_with_symbols(self) -> None:
        """Test parsing chain with symbols."""
        content = """
symbols:
  lambda: 1.5
  mu: 2.0
chain:
  - from: "S0"
    to: "S1"
    value: "lambda"
  - from: "S1"
    to: "S0"
    value: "mu"
"""
        mc = self.parser.parse(content)

        assert len(mc.symbols) == 2
        assert mc.symbols["lambda"] == 1.5
        assert mc.symbols["mu"] == 2.0

    def test_parse_json_format(self) -> None:
        """Test parsing JSON format."""
        content = '{"chain": [{"from": "A", "to": "B", "value": "0.5"}]}'
        mc = self.parser.parse(content)

        assert len(mc.states) == 2
        assert len(mc.links) == 1

    def test_parse_invalid_yaml(self) -> None:
        """Test parsing invalid YAML raises ParserError."""
        content = "chain:\n  - from: [invalid"
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

    def test_parse_missing_chain_field(self) -> None:
        """Test parsing without chain field raises ParserError."""
        content = "symbols:\n  x: 1.0"
        with pytest.raises(ParserError, match="Invalid chain definition"):
            self.parser.parse(content)

    def test_parse_invalid_link_missing_from(self) -> None:
        """Test parsing link without 'from' raises ParserError."""
        content = """
chain:
  - to: "S1"
    value: "0.5"
"""
        with pytest.raises(ParserError, match="Invalid chain definition"):
            self.parser.parse(content)

    def test_parse_invalid_link_missing_to(self) -> None:
        """Test parsing link without 'to' raises ParserError."""
        content = """
chain:
  - from: "S0"
    value: "0.5"
"""
        with pytest.raises(ParserError, match="Invalid chain definition"):
            self.parser.parse(content)

    def test_parse_invalid_link_missing_value(self) -> None:
        """Test parsing link without 'value' raises ParserError."""
        content = """
chain:
  - from: "S0"
    to: "S1"
"""
        with pytest.raises(ParserError, match="Invalid chain definition"):
            self.parser.parse(content)

    def test_supports_extension_yaml(self) -> None:
        """Test supports_extension for .yaml."""
        assert self.parser.supports_extension(".yaml") is True
        assert self.parser.supports_extension(".YAML") is True

    def test_supports_extension_yml(self) -> None:
        """Test supports_extension for .yml."""
        assert self.parser.supports_extension(".yml") is True
        assert self.parser.supports_extension(".YML") is True

    def test_supports_extension_json(self) -> None:
        """Test supports_extension for .json."""
        assert self.parser.supports_extension(".json") is True
        assert self.parser.supports_extension(".JSON") is True

    def test_supports_extension_unsupported(self) -> None:
        """Test supports_extension for unsupported extensions."""
        assert self.parser.supports_extension(".txt") is False
        assert self.parser.supports_extension(".csv") is False
        assert self.parser.supports_extension(".dot") is False

    def test_parse_self_loop(self) -> None:
        """Test parsing chain with self-loop."""
        content = """
chain:
  - from: "S0"
    to: "S0"
    value: "0.5"
"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 1
        assert len(mc.links) == 1

    def test_parse_symbols_with_string_values(self) -> None:
        """Test parsing symbols with string numeric values."""
        content = """
symbols:
  rate: "3.14"
chain:
  - from: "S0"
    to: "S1"
    value: "rate"
"""
        mc = self.parser.parse(content)

        assert mc.symbols["rate"] == 3.14

    def test_parse_symbols_with_int_values(self) -> None:
        """Test parsing symbols with integer values."""
        content = """
symbols:
  count: 5
chain:
  - from: "S0"
    to: "S1"
    value: "count"
"""
        mc = self.parser.parse(content)

        assert mc.symbols["count"] == 5.0
