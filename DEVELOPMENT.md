# Development

## Prerequisites

- Python 3.12, 3.13 or 3.14 — see [Python versions](#python-versions).
  The default is 3.14: `make setup` pins the release named in the `Makefile`,
  and tox, mypy and the single-version CI jobs run on it.
- [pyenv](https://github.com/pyenv/pyenv) with the
  [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) plugin, used by
  `make setup` to create the virtualenv.
- [Homebrew](https://brew.sh/), used by `make setup` to install Graphviz.

## Setup

Setup development environment:

```shell
make setup
```

## Validate
Run tests and linters:

```shell
# Run all tests and linting with tox
tox

# Run specific environments
tox -e test        # Unit tests on the default interpreter
tox -e coverage    # Code coverage report
tox -e lint        # Linting only
tox -e type        # Type checking only
tox -e format      # Format code
```

### Python versions

markov-solver supports Python 3.12, 3.13 and 3.14. `tox` runs the suite on each
of them:

```shell
tox -e py312       # Run the suite on a single version
tox -e py312,py313,py314
```

Every other tox environment (`test`, `lint`, `type`, `format`, `coverage`) runs
on the default interpreter, 3.14, declared as `default_base_python` in `tox.ini`.
Black formats for every supported version so it never emits syntax 3.12
rejects; mypy checks against the default.

tox does not install interpreters, it only discovers them, and it fails rather
than skipping when one is missing. Install the versions you do not have first —
with pyenv:

```shell
pyenv install 3.12 3.13 3.14
```

pyenv only exposes the interpreter selected by `.python-version`, so put the
others on `PATH` before running the matrix:

```shell
export PATH="$HOME/.pyenv/versions/3.12.13/bin:$HOME/.pyenv/versions/3.13.13/bin:$PATH"
```

The supported range is declared once, in `SUPPORTED_PYTHON_VERSIONS` in
[tests/markov_solver/test_package.py](tests/markov_solver/test_package.py),
next to `DEFAULT_PYTHON_VERSION`. Tests fail if the PyPI classifiers,
`requires-python`, the black and mypy targets, `tox.ini`, the CI workflows, the
`Makefile` or the README badge disagree with them, so adding a version means
updating all of them alongside the constant.

The PR check runs the unit tests on every supported version and, once, linting,
type checking and the coverage gate on the default one.

## Documentation

Generate the CLI reference documentation using Sphinx:

```shell
make build-docs
```

The generated documentation will be in `docs/_build/html/`.

View the documentation:

```shell
make open-docs
```

Clean the documentation:

```shell
make clean-docs
```

## Release

Update version in `VERSION`

Draft the release

```shell
VERSION="$(cat VERSION)"
gh release create v${VERSION} \
   --title v${VERSION} \
   --target main \
   --notes-file CHANGELOG.md \
   --latest \
   --draft
```

Make changes to the release notes, and publish

```shell
gh release edit v${VERSION} --draft=false
```

This will automatically publish to PyPI at https://pypi.org/project/markov-solver.

### Demo
The product demo is a video that emulates the terminal behavior.
The video is generated with [Terminalizer](https://www.terminalizer.com/).
To generate the vide:
```
nvm use 20
npm install -g node-gyp terminalizer
terminalizer render resources/brand/demo.yml --output resources/brand/demo.mp4
```
