# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Parser for CSV adjacency matrix format."""

import csv
import io

from markov_solver.core.model.markov_chain import MarkovChain
from markov_solver.core.model.markov_link import MarkovLink
from markov_solver.core.model.markov_state import MarkovState
from markov_solver.core.parser.base import FormatParser, ParserError


class CsvAdjacencyMatrixParser(FormatParser):
    """Parser for CSV adjacency matrix format.

    The first row and first column contain state names.
    Cell values are transition probabilities.

    Example:
        ,S0,S1,S2
        S0,0.5,0.5,0
        S1,0,0,1.0
        S2,0,0,1.0
    """

    def parse(self, content: str) -> MarkovChain:
        mc = MarkovChain()

        reader = csv.reader(io.StringIO(content))
        rows = list(reader)

        if len(rows) < 2:
            raise ParserError("CSV must have at least a header row and one data row")

        # First row is header with state names (first cell may be empty)
        header = rows[0]
        states = [s.strip() for s in header[1:] if s.strip()]

        if not states:
            raise ParserError("No states found in CSV header")

        # Add all states
        for state_name in states:
            mc.add_state(MarkovState(state_name))

        # Process data rows
        for row in rows[1:]:
            if not row:
                continue

            from_state = row[0].strip()
            if not from_state:
                continue

            for i, value in enumerate(row[1:]):
                if i >= len(states):
                    break

                value = value.strip()
                if not value or value == "0" or value == "0.0":
                    continue

                to_state = states[i]
                head = MarkovState(from_state)
                tail = MarkovState(to_state)
                mc.add_link(MarkovLink(head, tail, value))

        return mc

    def supports_extension(self, extension: str) -> bool:
        return extension.lower() == ".csv"
