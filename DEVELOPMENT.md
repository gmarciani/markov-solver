# Markov Solver -- Development

## Requirements
```
pyenv virtualenv 3.10.13 markov-solver-dev
pyenv activate markov-solver-dev
pip install --upgrade pip
pip install -r requirements-dev.txt
```

## Configure PreCommit
Install pre-commit hook for the local repo:
```
pre-commit install
```

For the first time, run pre-commit checks on the whole codebase:
```
pre-commit run --all-files
```

## Build
```
python -m build
```

## Publish
To publish a new release on PyPI, you need to create a new release on GitHub, 
which in turns triggers a GitHub action to publish the release on PyPI.

To this aim, you first need to store the PyPI API Token as a secret on GitHub:

```
PYPI_API_TOKEN_BODY=$(cat resources/secrets/pypi-token.txt)
gh secret set "PYPI_API_TOKEN" \
  --app "actions" \
  --body "${PYPI_API_TOKEN_BODY}"
```

Create a draft release:

```
VERSION="1.0.0"
gh release create v${VERSION} \
--title "markov-solver v$VERSION" \
--target mainline \
--notes-file CHANGELOG.md \
--latest \
--draft
```

Make changes to the release notes.

Publish the release:

```
gh release edit v${VERSION} --draft=false
```

If you need to delete the release from GitHub:

```
gh release delete v${VERSION} --cleanup-tag --yes
```

### Manually publish to PyPI test
Publish to PyPi test repo at https://test.pypi.org/project/markov-solver
```
python -m twine upload --repository testpypi dist/*
```

### Manually publish to PyPI prod
Publish to PyPi production repo at https://pypi.org/project/markov-solver
```
python -m twine upload dist/*
```