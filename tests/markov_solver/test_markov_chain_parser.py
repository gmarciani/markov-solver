# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Tests for MarkovChainParser and helper functions."""

import tempfile
from pathlib import Path

import pytest

from markov_solver.core.parser.base import FormatParser, ParserError
from markov_solver.core.parser.markov_chain_parser import (
    MarkovChainParser,
    create_chain_from_file,
    create_chain_from_string,
    get_parser,
)
from markov_solver.core.model.markov_chain import MarkovChain


class TestMarkovChainParser:
    """Tests for MarkovChainParser."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.parser = MarkovChainParser()

    def test_init_registers_default_parsers(self) -> None:
        """Test that default parsers are registered on init."""
        assert len(self.parser._format_parsers) == 3

    def test_register_parser(self) -> None:
        """Test registering a custom parser."""
        initial_count = len(self.parser._format_parsers)

        class CustomParser(FormatParser):
            def parse(self, content: str) -> MarkovChain:
                return MarkovChain()

            def supports_extension(self, extension: str) -> bool:
                return extension == ".custom"

        self.parser.register_parser(CustomParser())
        assert len(self.parser._format_parsers) == initial_count + 1

    def test_parse_file_yaml(self) -> None:
        """Test parsing a YAML file."""
        content = """
chain:
  - from: "S0"
    to: "S1"
    value: "0.5"
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(content)
            f.flush()
            mc = self.parser.parse_file(f.name)

        assert len(mc.states) == 2
        Path(f.name).unlink()

    def test_parse_file_not_found(self) -> None:
        """Test parsing non-existent file raises ParserError."""
        with pytest.raises(ParserError, match="File not found"):
            self.parser.parse_file("/nonexistent/path/file.yaml")

    def test_parse_file_unsupported_extension(self) -> None:
        """Test parsing file with unsupported extension raises ParserError."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xyz", delete=False) as f:
            f.write("content")
            f.flush()
            with pytest.raises(ParserError, match="Unsupported file extension"):
                self.parser.parse_file(f.name)
            Path(f.name).unlink()

    def test_parse_string_default_parser(self) -> None:
        """Test parse_string uses ChainFormatParser by default."""
        content = """
chain:
  - from: "A"
    to: "B"
    value: "1.0"
"""
        mc = self.parser.parse_string(content)
        assert len(mc.states) == 2

    def test_parse_string_custom_parser(self) -> None:
        """Test parse_string with custom parser."""
        from markov_solver.core.parser.dot_parser import DotParser

        content = "A -> B [label=0.5]"
        mc = self.parser.parse_string(content, format_parser=DotParser())
        assert len(mc.states) == 2


class TestCreateChainFromFile:
    """Tests for create_chain_from_file function."""

    def test_create_chain_from_yaml_file(self) -> None:
        """Test creating chain from YAML file."""
        content = """
chain:
  - from: "X"
    to: "Y"
    value: "0.5"
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(content)
            f.flush()
            mc = create_chain_from_file(f.name)

        assert len(mc.states) == 2
        Path(f.name).unlink()

    def test_create_chain_from_path_object(self) -> None:
        """Test creating chain from Path object."""
        content = """
chain:
  - from: "A"
    to: "B"
    value: "1.0"
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(content)
            f.flush()
            mc = create_chain_from_file(Path(f.name))

        assert len(mc.states) == 2
        Path(f.name).unlink()


class TestCreateChainFromString:
    """Tests for create_chain_from_string function."""

    def test_create_chain_format(self) -> None:
        """Test creating chain with chain format."""
        content = """
chain:
  - from: "A"
    to: "B"
    value: "0.5"
"""
        mc = create_chain_from_string(content, format_type="chain")
        assert len(mc.states) == 2

    def test_create_matrix_format(self) -> None:
        """Test creating chain with matrix format."""
        content = """
states:
  - A
  - B
transitions:
  A:
    B: 1.0
"""
        mc = create_chain_from_string(content, format_type="matrix")
        assert len(mc.states) == 2

    def test_create_dot_format(self) -> None:
        """Test creating chain with DOT format."""
        content = "A -> B [label=0.5]"
        mc = create_chain_from_string(content, format_type="dot")
        assert len(mc.states) == 2

    def test_create_csv_format(self) -> None:
        """Test creating chain with CSV format."""
        content = """,A,B
A,0,1.0
B,0.5,0"""
        mc = create_chain_from_string(content, format_type="csv")
        assert len(mc.states) == 2

    def test_create_unknown_format(self) -> None:
        """Test creating chain with unknown format raises ParserError."""
        with pytest.raises(ParserError, match="Unknown format type"):
            create_chain_from_string("content", format_type="unknown")


class TestGetParser:
    """Tests for get_parser function."""

    def test_get_parser_returns_instance(self) -> None:
        """Test get_parser returns MarkovChainParser instance."""
        parser = get_parser()
        assert isinstance(parser, MarkovChainParser)

    def test_get_parser_returns_same_instance(self) -> None:
        """Test get_parser returns the same default instance."""
        parser1 = get_parser()
        parser2 = get_parser()
        assert parser1 is parser2
