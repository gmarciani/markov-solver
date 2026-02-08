# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Tests for DotParser."""

import pytest

from markov_solver.core.parser.dot_parser import DotParser
from markov_solver.core.parser.base import ParserError


class TestDotParser:
    """Tests for DotParser."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.parser = DotParser()

    def test_parse_simple_digraph(self) -> None:
        """Test parsing a simple digraph."""
        content = """digraph {
    S0 -> S1 [label=0.5]
    S1 -> S2 [label=1.0]
}"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 3
        assert len(mc.links) == 2

    def test_parse_with_self_loop(self) -> None:
        """Test parsing digraph with self-loop."""
        content = """digraph {
    S0 -> S0 [label=0.5]
    S0 -> S1 [label=0.5]
}"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 2
        assert len(mc.links) == 2

    def test_parse_quoted_labels(self) -> None:
        """Test parsing with quoted label values."""
        content = """digraph {
    S0 -> S1 [label="0.5"]
    S1 -> S2 [label="1.0"]
}"""
        mc = self.parser.parse(content)

        assert len(mc.links) == 2

    def test_parse_quoted_node_names(self) -> None:
        """Test parsing with quoted node names (no spaces)."""
        content = """digraph {
    "S0" -> "S1" [label=0.5]
}"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 2

    def test_parse_without_labels(self) -> None:
        """Test parsing edge without label defaults to 1.0."""
        content = """digraph {
    S0 -> S1
}"""
        mc = self.parser.parse(content)

        assert len(mc.links) == 1
        for link in mc.links:
            assert link.value == "1.0"

    def test_parse_mixed_labels(self) -> None:
        """Test parsing with edge having label."""
        content = """digraph {
    S0 -> S1 [label=0.5]
}"""
        mc = self.parser.parse(content)

        assert len(mc.links) == 1

    def test_parse_symbolic_labels(self) -> None:
        """Test parsing with symbolic label values."""
        content = """digraph {
    S0 -> S1 [label=lambda]
    S1 -> S0 [label=mu]
}"""
        mc = self.parser.parse(content)

        links = list(mc.links)
        values = {link.value for link in links}
        assert "lambda" in values
        assert "mu" in values

    def test_parse_no_edges(self) -> None:
        """Test parsing content with no edges raises ParserError."""
        content = """digraph {
    // just a comment
}"""
        with pytest.raises(ParserError, match="No valid edges found in DOT file"):
            self.parser.parse(content)

    def test_parse_empty_content(self) -> None:
        """Test parsing empty content raises ParserError."""
        with pytest.raises(ParserError, match="No valid edges found in DOT file"):
            self.parser.parse("")

    def test_parse_invalid_content(self) -> None:
        """Test parsing invalid content raises ParserError."""
        content = "this is not a valid DOT file"
        with pytest.raises(ParserError, match="No valid edges found in DOT file"):
            self.parser.parse(content)

    def test_parse_expression_labels(self) -> None:
        """Test parsing with expression labels."""
        content = """digraph {
    S0 -> S1 [label="lambda+mu"]
}"""
        mc = self.parser.parse(content)

        link = list(mc.links)[0]
        assert link.value == "lambda+mu"

    def test_parse_whitespace_handling(self) -> None:
        """Test parsing handles various whitespace."""
        content = """digraph {
    S0->S1[label=0.5]
    S2  ->  S3  [  label  =  0.7  ]
}"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 4
        assert len(mc.links) == 2

    def test_supports_extension_dot(self) -> None:
        """Test supports_extension for .dot."""
        assert self.parser.supports_extension(".dot") is True
        assert self.parser.supports_extension(".DOT") is True

    def test_supports_extension_gv(self) -> None:
        """Test supports_extension for .gv."""
        assert self.parser.supports_extension(".gv") is True
        assert self.parser.supports_extension(".GV") is True

    def test_supports_extension_unsupported(self) -> None:
        """Test supports_extension for unsupported extensions."""
        assert self.parser.supports_extension(".yaml") is False
        assert self.parser.supports_extension(".json") is False
        assert self.parser.supports_extension(".csv") is False
        assert self.parser.supports_extension(".txt") is False

    def test_parse_graph_keyword(self) -> None:
        """Test parsing works without digraph keyword."""
        content = """
    A -> B [label=0.5]
    B -> C [label=1.0]
"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 3
        assert len(mc.links) == 2

    def test_parse_numeric_state_names(self) -> None:
        """Test parsing with numeric state names."""
        content = """digraph {
    0 -> 1 [label=0.5]
    1 -> 2 [label=1.0]
}"""
        mc = self.parser.parse(content)

        assert len(mc.states) == 3
        assert len(mc.links) == 2
