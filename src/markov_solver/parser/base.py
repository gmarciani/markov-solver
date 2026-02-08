# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Base classes for Markov chain parsers."""

from abc import ABC, abstractmethod

from markov_solver.model.markov_chain import MarkovChain


class ParserError(Exception):
    """Raised when parsing fails."""


class FormatParser(ABC):
    """Abstract base class for format-specific parsers."""

    @abstractmethod
    def parse(self, content: str) -> MarkovChain:
        """Parse file content into a MarkovChain."""

    @abstractmethod
    def supports_extension(self, extension: str) -> bool:
        """Check if this parser supports the given file extension."""
