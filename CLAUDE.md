# CLAUDE.md

`markov-solver`: steady-state solver for Markov chains defined in YAML/JSON, DOT or CSV, with symbolic rates. CLI + library, src-layout under `src/markov_solver`.

## Commands

```shell
make setup                 # pyenv venv + Graphviz + editable install
tox                        # test, lint, type, coverage
tox -e test|lint|type|format
pytest tests/ -v           # fast iteration
make build-docs            # Sphinx -> docs/_build/html/
```

## Conventions

- Pipeline: definition file → `parser/` (`FormatParser` registry in `markov_chain_parser.py`) → `model/MarkovChain` → `solve()` → `results/SimpleReport`.
- All parse failures raise `parser.base.ParserError`. Chain and matrix formats share YAML/JSON extensions and are told apart by `FormatParser.supports_content`.
- Tests mirror the package layout under `tests/markov_solver/`, use `assertpy` and `pytest-resource-path` (fixtures in `tests/resources/`).
- mypy is strict: every new function needs full type annotations.
- Release: bump `VERSION`, update `CHANGELOG.md` (enforced in CI), then `gh release create`.
