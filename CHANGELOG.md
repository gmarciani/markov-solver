# Changelog

All notable changes to CLI Wizard will be documented in this file.

## 2.0.0

### New Features
- Added support for multiple input formats to define Markov chains:
  - DOT/Graphviz format (.dot, .gv)
  - CSV adjacency matrix format (.csv)
  - Transition matrix YAML/JSON format

### Improvements
- Added comprehensive type annotations across all source files.
- Added Pydantic-based validation for input files.
- Increased test coverage to 90%+ with new test files for all modules.
- Added public documentation based on Sphinx.

### Changes
- Migrated from `setup.py` to modern `pyproject.toml` packaging.
- Upgraded click to version 8.3.1.
- Upgraded colored to version 2.3.1.
- Upgraded graphviz to version 0.21.
- Upgraded networkx to version 3.6.1.
- Upgraded numpy to version 2.4.2.
- Upgraded pyfiglet to version 1.0.4.
- Upgraded pyyaml to version 6.0.3.
- Upgraded scipy to version 1.17.0.
- Upgraded sympy to version 1.14.0.

## 1.0.1

### Bug Fixes
- Fixed incomplete ordering in MarkovState and MarkovLink.

### Improvements
- Added a real example to show how to use the library.

### Changes
- Upgraded `click` to version 8.1.7.
- Upgraded `colored` to version 2.2.4.
- Upgraded `graphviz` to version 0.20.3.
- Upgraded `networkx` to version 3.2.1.
- Upgraded `numpy` to version 2.0.1.
- Upgraded `pyfiglet` to version 1.0.2.
- Upgraded `pyyaml` to version 6.0.2.
- Upgraded `scipy` to version 1.13.1.
- Upgraded `setuptools` to version 72.1.0.
- Upgraded `sympy` to version 1.13.1.


## 1.0.0

- First public release


## 0.0.4

- Add images for chain examples in README


## 0.0.3

- Add rendering of Markov chains
- Add examples: simple and symbolic


## 0.0.2

- Add support for symbolic Markov chains


## 0.0.1

- Release on GitHub and PyPi
