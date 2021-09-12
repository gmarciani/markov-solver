# Markov Solver -- Development

## Requirements
```
pip install --upgrade pip
pip install --upgrade build twine
```

## Build
```
python -m build
```

## Publish
```
python -m twine upload --repository testpypi dist/*
```
