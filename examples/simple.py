from markov_solver.core.parser.markov_chain_parser import create_chain_from_file
from markov_solver.utils.report import SimpleReport as Report
from os import path

definition = path.join(path.dirname(path.abspath(__file__)), "simple.definition.yaml")
markov_chain = create_chain_from_file(definition)
states_probabilities = markov_chain.solve()

report = Report("MARKOV CHAIN SOLUTION")
for state in sorted(states_probabilities):
    report.add("states probability", state, states_probabilities[state])

print(report)
