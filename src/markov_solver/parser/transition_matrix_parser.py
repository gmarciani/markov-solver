# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Parser for transition matrix YAML/JSON format."""

import yaml
from pydantic import ValidationError

from markov_solver.model.markov_chain import MarkovChain
from markov_solver.model.markov_link import MarkovLink
from markov_solver.model.markov_state import MarkovState
from markov_solver.parser.base import FormatParser, ParserError
from markov_solver.parser.schema import TransitionMatrixDefinition


class TransitionMatrixParser(FormatParser):
    """Parser for transition matrix YAML/JSON format.

    Example:
        {
            "states": ["S0", "S1", "S2"],
            "transitions": {
                "S0": {"S0": 0.5, "S1": 0.5},
                "S1": {"S2": 1.0}
            }
        }
    """

    def parse(self, content: str) -> MarkovChain:
        try:
            raw_data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ParserError(f"Invalid YAML/JSON: {e}") from e

        if not raw_data:
            raise ParserError("Empty definition file")

        try:
            definition = TransitionMatrixDefinition.model_validate(raw_data)
        except ValidationError as e:
            errors = "; ".join(
                f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}"
                for err in e.errors()
            )
            raise ParserError(f"Invalid transition matrix: {errors}") from e

        return self._build_chain(definition)

    def _build_chain(self, definition: TransitionMatrixDefinition) -> MarkovChain:
        mc = MarkovChain()

        if definition.symbols:
            # Convert all symbol values to float
            symbols = {k: float(v) for k, v in definition.symbols.items()}
            mc.add_symbols(**symbols)

        # Add all states
        for state_name in definition.states:
            mc.add_state(MarkovState(state_name))

        # Add transitions
        for from_state, targets in definition.transitions.items():
            head = MarkovState(from_state)
            for to_state, value in targets.items():
                tail = MarkovState(to_state)
                link = MarkovLink(head, tail, str(value))
                mc.add_link(link)

        return mc

    def supports_extension(self, extension: str) -> bool:
        # This parser handles the same extensions but different schema
        return False  # Not auto-detected, must be explicitly used
