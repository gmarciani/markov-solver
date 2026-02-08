# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Parser for DOT/Graphviz format."""

import re

from markov_solver.model.markov_chain import MarkovChain
from markov_solver.model.markov_link import MarkovLink
from markov_solver.model.markov_state import MarkovState
from markov_solver.parser.base import FormatParser, ParserError


class DotParser(FormatParser):
    """Parser for DOT/Graphviz format.

    Example::

        digraph {
            S0 -> S0 [label=0.5]
            S0 -> S1 [label=0.5]
            S1 -> S2 [label=1.0]
        }
    """

    # Pattern to match edges: node1 -> node2 [label=value] or [label="value"]
    EDGE_PATTERN = re.compile(
        r'^\s*"?([^"\s\->]+)"?\s*->\s*"?([^"\s\[]+)"?\s*'
        r'(?:\[\s*label\s*=\s*"?([^"\]]+)"?\s*\])?',
        re.MULTILINE,
    )

    def parse(self, content: str) -> MarkovChain:
        mc = MarkovChain()

        # Find all edges
        matches = self.EDGE_PATTERN.findall(content)

        if not matches:
            raise ParserError("No valid edges found in DOT file")

        for from_state, to_state, label in matches:
            from_state = from_state.strip()
            to_state = to_state.strip()
            value = label.strip() if label else "1.0"

            head = MarkovState(from_state)
            tail = MarkovState(to_state)
            mc.add_state(head)
            mc.add_state(tail)
            mc.add_link(MarkovLink(head, tail, value))

        return mc

    def supports_extension(self, extension: str) -> bool:
        return extension.lower() in {".dot", ".gv"}
