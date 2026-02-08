Definition Formats
==================

Markov Solver supports multiple input formats for defining Markov chains.
This page documents each supported format with examples and schema references.

See the `examples directory <https://github.com/gmarciani/markov-chain/tree/mainline/examples>`_ for complete configuration examples.

Supported Formats
-----------------

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Format
     - Extensions
     - Description
   * - Chain Format
     - ``.yaml``, ``.yml``, ``.json``
     - List of transitions with from/to/value fields
   * - Transition Matrix
     - ``.yaml``, ``.yml``, ``.json``
     - States list with nested transition probabilities
   * - DOT/Graphviz
     - ``.dot``, ``.gv``
     - Standard Graphviz directed graph format
   * - CSV Adjacency Matrix
     - ``.csv``
     - Spreadsheet-compatible adjacency matrix

Chain Format (YAML/JSON)
------------------------

The chain format defines a Markov chain as a list of transitions.
This is the default format for ``.yaml``, ``.yml``, and ``.json`` files.

Schema
~~~~~~

.. autopydantic_model:: markov_solver.core.parser.schema.MarkovChainDefinition

.. autopydantic_model:: markov_solver.core.parser.schema.MarkovLinkSchema

Example (YAML)
~~~~~~~~~~~~~~

.. code-block:: yaml

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

Example with Symbols (YAML)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    symbols:
      lambda: 1.5
      mu: 2.0
    chain:
      - from: "S0"
        to: "S1"
        value: "lambda"
      - from: "S1"
        to: "S0"
        value: "mu"

Transition Matrix Format
------------------------

The transition matrix format defines states explicitly and uses nested
dictionaries for transition probabilities.

Schema
~~~~~~

.. autopydantic_model:: markov_solver.core.parser.schema.TransitionMatrixDefinition

Example (YAML)
~~~~~~~~~~~~~~

.. code-block:: yaml

    states:
      - Sunny
      - Rainy
    transitions:
      Sunny:
        Sunny: 0.9
        Rainy: 0.1
      Rainy:
        Rainy: 0.5
        Sunny: 0.5

Example (JSON)
~~~~~~~~~~~~~~

.. code-block:: json

    {
      "states": ["Sunny", "Rainy"],
      "transitions": {
        "Sunny": {"Sunny": 0.9, "Rainy": 0.1},
        "Rainy": {"Rainy": 0.5, "Sunny": 0.5}
      }
    }


DOT/Graphviz Format
-------------------

The DOT format uses standard Graphviz syntax for directed graphs.
Edge labels represent transition probabilities.

Parser
~~~~~~

.. autoclass:: markov_solver.core.parser.dot_parser.DotParser
   :members:
   :undoc-members:
   :show-inheritance:

Example
~~~~~~~

.. code-block:: text

    digraph {
        Sunny -> Sunny [label=0.9]
        Sunny -> Rainy [label=0.1]
        Rainy -> Rainy [label=0.5]
        Rainy -> Sunny [label=0.5]
    }

Notes
~~~~~

- Node names can be quoted or unquoted
- Labels can be quoted or unquoted
- Edges without labels default to probability ``1.0``
- Symbolic values are supported in labels

CSV Adjacency Matrix Format
---------------------------

The CSV format represents the transition matrix as a spreadsheet-compatible
adjacency matrix.

Parser
~~~~~~

.. autoclass:: markov_solver.core.parser.csv_parser.CsvAdjacencyMatrixParser
   :members:
   :undoc-members:
   :show-inheritance:

Example
~~~~~~~

.. code-block:: text

    ,Sunny,Rainy
    Sunny,0.9,0.1
    Rainy,0.5,0.5

Notes
~~~~~

- First row contains state names (header)
- First column contains source state names
- Cell values are transition probabilities
- Zero values (``0`` or ``0.0``) are ignored
- Empty cells are ignored

Extensibility
-------------

The parser system is extensible. You can create custom parsers by
subclassing the ``FormatParser`` base class.

Base Class
~~~~~~~~~~

.. autoclass:: markov_solver.core.parser.base.FormatParser
   :members:
   :undoc-members:
   :show-inheritance:

.. autoexception:: markov_solver.core.parser.base.ParserError
   :show-inheritance:

Registering Custom Parsers
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from markov_solver.core.parser import get_parser, FormatParser
    from markov_solver.core.model.markov_chain import MarkovChain

    class MyCustomParser(FormatParser):
        def parse(self, content: str) -> MarkovChain:
            # Custom parsing logic
            ...

        def supports_extension(self, extension: str) -> bool:
            return extension.lower() == ".custom"

    # Register the parser
    parser = get_parser()
    parser.register_parser(MyCustomParser())
