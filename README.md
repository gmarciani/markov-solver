# Markov Solver
*Utility to solve Markov Chains.*

## Requirements
* Python 3.6+

## Install
Install all required packages with PIP, running:
```shell
pip install markov-solver
```

## Usage
Let us image that we want to solve the following Markov chain:

![Markov Chain Simple](resources/definitions/simple/simple.png)

We should create a YAML file that defines the chain:
```yaml
symbols:
  L: 1.0

chain:
  - from: "Sunny"
    to: "Sunny"
    value: "0.9*L"

  - from: "Sunny"
    to: "Rainy"
    value: "0.1*L"

  - from: "Rainy"
    to: "Rainy"
    value: "0.5*L"

  - from: "Rainy"
    to: "Sunny"
    value: "0.5*L"
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

## Authors
Giacomo Marciani, [mgiacomo@amazon.com](mailto:mgiacomo@amazon.com)

## References
* "Discrete-Event Simulation", 2006, L.M. Leemis, S.K. Park
* "Performance Modeling and Design of Computer Systems, 2013, M. Harchol-Balter

## License
The project is released under the [MIT License](https://opensource.org/licenses/MIT).
