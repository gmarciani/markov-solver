# Changelog

## 2.1.0

### Bug Fixes
- Definition files can no longer execute arbitrary code: transition values are parsed as plain arithmetic
  (numbers, symbols, `+ - * / **`, parentheses) instead of being evaluated as Python.
- Fixed silently wrong probabilities when a symbol name was a prefix of another (`mu` in `mu2`) or of a numeric
  literal (`e` in `1e-1`): symbols are now substituted by whole name.
- A transition declared twice between the same two states is now rejected as a duplicate, instead of having
  its rates silently summed.
- Chains with no steady-state solution (no transitions, negative rates, dead-end states) now fail with a clear
  error instead of a crash.
- Transition matrix definitions in `.yaml`, `.yml` and `.json` files are now detected automatically, as documented.
- Unquoted YAML/JSON numbers are now accepted for `from`, `to` and `value` in the chain format (e.g. `from: 0`).
- Undefined symbols and non-numeric symbol values (e.g. `rate: fast`) are reported with a clear error naming
  the symbol.
- Invalid definition files are reported by the CLI as a one-line error with exit code 1, instead of a traceback.
- The `--debug` flag now enables debug logging.
- Fixed the package description shown on PyPI.

### Changes
- Expressed all dependencies with the `~=` version constraint pinned to the minor version,
  so patch-level updates are applied automatically while minor/major upgrades remain explicit.
- Upgraded autoflake to version 2.4.0.
- Upgraded black to version 26.5.1.
- Upgraded build to version 1.6.1.
- Upgraded click to version 8.5.0.
- Upgraded colored to version 2.3.2.
- Upgraded flake8 to version 7.4.1.
- Upgraded graphviz to version 0.21.0.
- Upgraded mypy to version 2.3.1.
- Upgraded networkx to version 3.7.0.
- Upgraded numpy to version 2.5.3.
- Upgraded pre-commit to version 4.6.2.
- Upgraded pydantic to version 2.13.5.
- Upgraded pytest to version 9.1.1.
- Upgraded pytest-cov to version 7.1.0.
- Upgraded pytest-resource-path to version 1.5.0.
- Upgraded scipy to version 1.18.1.
- Upgraded sphinx-new-tab-link to version 0.8.2.
- Upgraded tox to version 4.64.3.
- Upgraded twine to version 7.0.0.
- Upgraded types-PyYAML to version 6.0.12.
- Upgraded types-requests to version 2.33.0.

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
