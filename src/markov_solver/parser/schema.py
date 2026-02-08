# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Pydantic schemas for Markov chain definition files."""

from pydantic import BaseModel, Field


class MarkovLinkSchema(BaseModel):
    """Schema for a single link/edge in the Markov chain."""

    from_state: str = Field(..., alias="from", description="Source state name")
    to_state: str = Field(..., alias="to", description="Target state name")
    value: str = Field(..., description="Transition probability or rate")

    model_config = {"populate_by_name": True}


class MarkovChainDefinition(BaseModel):
    """Schema for the chain-based Markov chain definition format.

    Example::

        chain:
          - from: "S0"
            to: "S1"
            value: "0.5"
    """

    chain: list[MarkovLinkSchema] = Field(
        ..., description="List of links defining the Markov chain"
    )
    symbols: dict[str, str | int | float] = Field(
        default_factory=dict, description="Optional symbolic variables"
    )


class TransitionMatrixDefinition(BaseModel):
    """Schema for the transition matrix Markov chain definition format.

    Example::

        {
            "states": ["S0", "S1", "S2"],
            "initial": "S0",
            "transitions": {
                "S0": {"S0": 0.5, "S1": 0.5},
                "S1": {"S2": 1.0}
            }
        }
    """

    states: list[str] = Field(..., description="List of state names")
    transitions: dict[str, dict[str, float | str]] = Field(
        ..., description="Transition matrix as nested dict"
    )
    initial: str | None = Field(default=None, description="Optional initial state")
    symbols: dict[str, str | int | float] = Field(
        default_factory=dict, description="Optional symbolic variables"
    )
