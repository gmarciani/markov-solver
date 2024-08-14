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

## Configure secrets
```
PYPI_API_TOKEN_BODY=$(cat resources/secrets/pypi-token.txt)
gh secret set "PYPI_API_TOKEN" \
  --app "actions" \
  --body "${PYPI_API_TOKEN_BODY}"
```

## Publish a new release
Create a draft release:
```
VERSION="1.0.1"
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

To delete a release from GitHub:
```
gh release delete v${VERSION} --cleanup-tag --yes
```