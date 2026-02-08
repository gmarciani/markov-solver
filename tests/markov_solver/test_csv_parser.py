# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Tests for CsvAdjacencyMatrixParser."""

import pytest

from markov_solver.core.parser.csv_parser import CsvAdjacencyMatrixParser
from markov_solver.core.parser.base import ParserError


class TestCsvAdjacencyMatrixParser:
    """Tests for CsvAdjacencyMatrixParser."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.parser = CsvAdjacencyMatrixParser()

    def test_parse_simple_matrix(self) -> None:
        """Test parsing a simple adjacency matrix."""
        content = """,S0,S1,S2
S0,0.5,0.5,0
S1,0,0,1.0
S2,0,0,1.0"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 3
        # S0->S0 (0.5), S0->S1 (0.5), S1->S2 (1.0), S2->S2 (1.0)
        assert len(mc.links) == 4

    def test_parse_with_zero_values(self) -> None:
        """Test that zero values are skipped."""
        content = """,A,B
A,0,1.0
B,0.5,0"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 2
        # A->B (1.0), B->A (0.5)
        assert len(mc.links) == 2

    def test_parse_with_zero_point_zero(self) -> None:
        """Test that 0.0 values are skipped."""
        content = """,A,B
A,0.0,1.0
B,0.5,0.0"""
        mc = self.parser.parse(content)

        assert len(mc.links) == 2

    def test_parse_empty_values_skipped(self) -> None:
        """Test that empty values are skipped."""
        content = """,A,B
A,,1.0
B,0.5,"""
        mc = self.parser.parse(content)

        assert len(mc.links) == 2

    def test_parse_too_few_rows(self) -> None:
        """Test parsing with only header row raises ParserError."""
        content = ",S0,S1,S2"
        with pytest.raises(
            ParserError, match="CSV must have at least a header row and one data row"
        ):
            self.parser.parse(content)

    def test_parse_empty_header(self) -> None:
        """Test parsing with no states in header raises ParserError."""
        content = """,,,
S0,0.5,0.5,0"""
        with pytest.raises(ParserError, match="No states found in CSV header"):
            self.parser.parse(content)

    def test_parse_empty_row_skipped(self) -> None:
        """Test that empty rows are skipped."""
        content = """,A,B
A,0,1.0

B,0.5,0"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 2
        assert len(mc.links) == 2

    def test_parse_row_with_empty_from_state(self) -> None:
        """Test that rows with empty from_state are skipped."""
        content = """,A,B
A,0,1.0
,0.5,0"""
        mc = self.parser.parse(content)

        assert len(mc.links) == 1

    def test_parse_extra_columns_ignored(self) -> None:
        """Test that extra columns beyond states are ignored."""
        content = """,A,B
A,0,1.0,extra
B,0.5,0,extra"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 2
        assert len(mc.links) == 2

    def test_parse_whitespace_trimmed(self) -> None:
        """Test that whitespace is trimmed from values."""
        content = """ , A , B
 A , 0 , 1.0
 B , 0.5 , 0 """
        mc = self.parser.parse(content)

        assert len(mc.states) == 2
        assert len(mc.links) == 2

    def test_parse_symbolic_values(self) -> None:
        """Test parsing with symbolic values."""
        content = """,A,B
A,0,lambda
B,mu,0"""
        mc = self.parser.parse(content)

        assert len(mc.links) == 2
        # Check that symbolic values are preserved as strings
        links = list(mc.links)
        values = {link.value for link in links}
        assert "lambda" in values
        assert "mu" in values

    def test_supports_extension_csv(self) -> None:
        """Test supports_extension for .csv."""
        assert self.parser.supports_extension(".csv") is True
        assert self.parser.supports_extension(".CSV") is True

    def test_supports_extension_unsupported(self) -> None:
        """Test supports_extension for unsupported extensions."""
        assert self.parser.supports_extension(".yaml") is False
        assert self.parser.supports_extension(".json") is False
        assert self.parser.supports_extension(".dot") is False
        assert self.parser.supports_extension(".txt") is False

    def test_parse_single_state(self) -> None:
        """Test parsing matrix with single state."""
        content = """,A
A,0.5"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 1
        assert len(mc.links) == 1

    def test_parse_no_transitions(self) -> None:
        """Test parsing matrix with no transitions (all zeros)."""
        content = """,A,B
A,0,0
B,0,0"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 2
        assert len(mc.links) == 0
