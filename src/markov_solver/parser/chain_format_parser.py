# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Parser for chain-based YAML/JSON format."""

import yaml
from pydantic import ValidationError

from markov_solver.model.markov_chain import MarkovChain
from markov_solver.model.markov_link import MarkovLink
from markov_solver.model.markov_state import MarkovState
from markov_solver.parser.base import FormatParser, ParserError
from markov_solver.parser.schema import MarkovChainDefinition


class ChainFormatParser(FormatParser):
    """Parser for chain-based YAML/JSON format.

    Example:
        chain:
          - from: "S0"
            to: "S1"
            value: "0.5"
    """

    def parse(self, content: str) -> MarkovChain:
        # Try YAML first (also handles JSON)
        try:
            raw_data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ParserError(f"Invalid YAML/JSON: {e}") from e

        if not raw_data:
            raise ParserError("Empty definition file")

        # Validate with Pydantic schema
        try:
            definition = MarkovChainDefinition.model_validate(raw_data)
        except ValidationError as e:
            errors = "; ".join(
                f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}"
                for err in e.errors()
            )
            raise ParserError(f"Invalid chain definition: {errors}") from e

        return self._build_chain(definition)

    def _build_chain(self, definition: MarkovChainDefinition) -> MarkovChain:
        mc = MarkovChain()

        if definition.symbols:
            # Convert all symbol values to float
            symbols = {k: float(v) for k, v in definition.symbols.items()}
            mc.add_symbols(**symbols)

        for link in definition.chain:
            head = MarkovState(link.from_state)
            tail = MarkovState(link.to_state)
            markov_link = MarkovLink(head, tail, link.value)
            mc.add_state(head)
            mc.add_state(tail)
            mc.add_link(markov_link)

        return mc

    def supports_extension(self, extension: str) -> bool:
        return extension.lower() in {".yaml", ".yml", ".json"}
