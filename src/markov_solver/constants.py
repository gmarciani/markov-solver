# Copyright (c) 2026, Giacomo Marciani
# Licensed under the MIT License

"""Constants."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("markov-solver")
except PackageNotFoundError:
    __version__ = "0.0.0"
