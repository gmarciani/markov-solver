# Markov Solver -- Development

## Requirements
```
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
Publish to PyPi test repo at https://test.pypi.org/project/markov-solver
```
python -m twine upload --repository testpypi dist/*
```

Publish to PyPi production repo at https://pypi.org/project/markov-solver
```
python -m twine upload dist/*
```

## Publish a new release
```
VERSION="1.0.1"
gh release create v${VERSION} \
--title "markov-solver v$VERSION" \
--target mainline \
--notes CHANGELOG.md \
--latest \
--draft
```

```
gh release edit v${VERSION} --draft=false
```