# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Main parser for Markov chain definition files."""

from pathlib import Path

from markov_solver.model.markov_chain import MarkovChain
from markov_solver.parser.base import FormatParser, ParserError
from markov_solver.parser.chain_format_parser import ChainFormatParser
from markov_solver.parser.csv_parser import CsvAdjacencyMatrixParser
from markov_solver.parser.dot_parser import DotParser
from markov_solver.parser.transition_matrix_parser import TransitionMatrixParser


class MarkovChainParser:
    """Extensible parser for Markov chain definition files."""

    def __init__(self) -> None:
        self._format_parsers: list[FormatParser] = []
        # Register default parsers
        self.register_parser(ChainFormatParser())
        self.register_parser(DotParser())
        self.register_parser(CsvAdjacencyMatrixParser())

    def register_parser(self, parser: FormatParser) -> None:
        """Register a new format parser."""
        self._format_parsers.append(parser)

    def _get_parser_for_extension(self, extension: str) -> FormatParser:
        """Get the appropriate parser for a file extension."""
        for parser in self._format_parsers:
            if parser.supports_extension(extension):
                return parser

        supported_exts: set[str] = set()
        for p in self._format_parsers:
            for ext in [".yaml", ".yml", ".json", ".dot", ".gv", ".csv"]:
                if p.supports_extension(ext):
                    supported_exts.add(ext)

        raise ParserError(
            f"Unsupported file extension: {extension}. "
            f"Supported: {', '.join(sorted(supported_exts))}"
        )

    def parse_file(self, path: str | Path) -> MarkovChain:
        """Parse a Markov chain definition file."""
        file_path = Path(path)

        if not file_path.exists():
            raise ParserError(f"File not found: {file_path}")

        format_parser = self._get_parser_for_extension(file_path.suffix)
        content = file_path.read_text()

        return format_parser.parse(content)

    def parse_string(
        self, content: str, format_parser: FormatParser | None = None
    ) -> MarkovChain:
        """Parse a Markov chain from a string.

        Args:
            content: The string content to parse.
            format_parser: Optional parser to use. If not provided,
                          tries ChainFormatParser.
        """
        if format_parser is None:
            format_parser = ChainFormatParser()

        return format_parser.parse(content)


# Default parser instance
_default_parser = MarkovChainParser()


def create_chain_from_file(path: str | Path) -> MarkovChain:
    """Create a MarkovChain from a definition file.

    Supports:
    - YAML/JSON chain format (.yaml, .yml, .json)
    - DOT/Graphviz format (.dot, .gv)
    - CSV adjacency matrix (.csv)

    Args:
        path: Path to the definition file.

    Returns:
        A MarkovChain instance.

    Raises:
        ParserError: If the file cannot be parsed or validated.
    """
    return _default_parser.parse_file(path)


def create_chain_from_string(content: str, format_type: str = "chain") -> MarkovChain:
    """Create a MarkovChain from a string.

    Args:
        content: The definition content as a string.
        format_type: One of "chain", "matrix", "dot", "csv".

    Returns:
        A MarkovChain instance.

    Raises:
        ParserError: If the content cannot be parsed.
    """
    parsers: dict[str, FormatParser] = {
        "chain": ChainFormatParser(),
        "matrix": TransitionMatrixParser(),
        "dot": DotParser(),
        "csv": CsvAdjacencyMatrixParser(),
    }

    if format_type not in parsers:
        raise ParserError(
            f"Unknown format type: {format_type}. "
            f"Supported: {', '.join(parsers.keys())}"
        )

    return parsers[format_type].parse(content)


def get_parser() -> MarkovChainParser:
    """Get the default parser instance for customization."""
    return _default_parser
