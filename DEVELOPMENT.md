# Markov Solver -- Development

## Requirements
```
pip install --upgrade pip
pip install --upgrade pre-commit build twine
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
Publish to PyPi test repo at https://test.pypi.org/project/markov-solver:
```
python -m twine upload --repository testpypi dist/*
```

Publish to PyPi production repo at https://pypi.org/project/markov-solver:
```
python -m twine upload dist/*
```
