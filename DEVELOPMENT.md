# Development

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
tox -e test        # Unit tests
tox -e coverage    # Code coverage report
tox -e lint        # Linting only
tox -e type        # Type checking only
tox -e format      # Format code
```

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
