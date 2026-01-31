.PHONY: setup install

PYTHON_VERSION = 3.14.2
VENV_NAME = markov-solver-dev

setup:
	pyenv install $(PYTHON_VERSION) --skip-existing
	pyenv virtualenv $(PYTHON_VERSION) $(VENV_NAME) --force
	pyenv local $(VENV_NAME)
	$$HOME/.pyenv/versions/$(VENV_NAME)/bin/python -m pip install --upgrade pip
	brew install graphviz
	pre-commit install
	pip install -e ".[dev]"

install:
	pip install -e .

install-docs:
	pip install -e ".[docs]"

build-docs: install-docs
	$(MAKE) -C docs html

clean: clean-docs

clean-docs: install-docs
	$(MAKE) -C docs clean

open-docs:
	open docs/_build/html/index.html
