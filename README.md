# CLI WIZARD

<div align="center">
<img src="https://raw.githubusercontent.com/gmarciani/markov-solver/main/resources/brand/banner.png" alt="markov-solver-banner" width="500">

[![PyPI version](https://img.shields.io/pypi/v/cli-wizard.svg)](https://pypi.org/project/markov-solver)
[![Python versions](https://img.shields.io/pypi/pyversions/cli-wizard.svg)](https://pypi.org/project/markov-solver)
[![License](https://img.shields.io/github/license/gmarciani/cli-wizard.svg)](https://github.com/gmarciani/markov-solver/blob/main/LICENSE)
[![Build status](https://img.shields.io/github/actions/workflow/status/gmarciani/cli-wizard/test.yml?branch=main)](https://github.com/gmarciani/markov-solver/actions)
[![Tests](https://img.shields.io/github/actions/workflow/status/gmarciani/cli-wizard/test.yml?branch=main&label=tests)](https://github.com/gmarciani/markov-solver/actions)
[![Coverage](https://img.shields.io/codecov/c/github/gmarciani/cli-wizard)](https://codecov.io/gh/gmarciani/markov-solver)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Downloads](https://img.shields.io/pypi/dm/cli-wizard.svg)](https://pypi.org/project/markov-solver)

</div>

Solve Markov Chains in a glance.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [References](#references)
- [Issues](#issues)
- [License](#license)

## Features

TBD

## Installation

```shell
pip install markov-solver
```

## Usage

You can use `markov-solver` as a CLI or as a library in your project.

To use it as a CLI, check the recorded demo:

![Markov Chain Solver Demo](https://raw.githubusercontent.com/gmarciani/markov-solver/mainline/resources/brand/demo.gif)

To use it as a library, you can check the [examples](./examples).

In both cases you need to define the Markov Chain to solve.
See the instructions below to know how to do it.

### Chain with constant transition rates
Let us image that we want to solve the following Markov chain:

![Markov Chain Simple](https://raw.githubusercontent.com/gmarciani/markov-solver/mainline/resources/definitions/simple/simple.graph.svg)

We should create a YAML file that defines the chain:
```yaml
chain:
  - from: "Sunny"
    to: "Sunny"
    value: "0.9"

  - from: "Sunny"
    to: "Rainy"
    value: "0.1"

  - from: "Rainy"
    to: "Rainy"
    value: "0.5"

  - from: "Rainy"
    to: "Sunny"
    value: "0.5"
```

Then, running the following command:
```shell
markov-solver solve --definition [PATH_TO_DEFINITION_FILE]
```

We obtain the following result:
```
===============================================================
                     MARKOV CHAIN SOLUTION
===============================================================

                      states probability
Rainy.........................................0.166666666666667
Sunny.........................................0.833333333333333
```

### Chain with symbolic transition rates
Let us image that we want to solve the following Markov chain:

![Markov Chain Symbolic](https://raw.githubusercontent.com/gmarciani/markov-solver/mainline/resources/definitions/symbolic/symbolic.graph.svg)

We should create a YAML file that defines the chain:
```yaml
symbols:
  lambda: 1.5
  mu: 2.0

chain:
  - from: "0"
    to: "1"
    value: "lambda"

  - from: "1"
    to: "2"
    value: "lambda"

  - from: "2"
    to: "3"
    value: "lambda"

  - from: "3"
    to: "2"
    value: "3*mu"

  - from: "2"
    to: "1"
    value: "2*mu"

  - from: "1"
    to: "0"
    value: "mu"
```

Then, running the following command:
```shell
markov-solver solve --definition [PATH_TO_DEFINITION_FILE]
```

We obtain the following result:
```
===============================================================
                     MARKOV CHAIN SOLUTION
===============================================================

                      states probability
0.............................................0.475836431226766
1.............................................0.356877323420074
2.............................................0.133828996282528
3............................................0.0334572490706320
```

## References
* ["Discrete-Event Simulation", 2006, L.M. Leemis, S.K. Park](https://www.amazon.com/Discrete-Event-Simulation-Lawrence-M-Leemis/dp/0131429175)
* ["Performance Modeling and Design of Computer Systems, 2013, M. Harchol-Balter](https://www.amazon.com/Modeling-Simulation-Discrete-Event-Systems-ebook/dp/B00EMB3MXA)

## Issues

Please report any issues or feature requests on the [GitHub Issues](https://github.com/gmarciani/cli-wizard/issues) page.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
