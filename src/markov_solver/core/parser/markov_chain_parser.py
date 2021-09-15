import yaml

from markov_solver.core.model.markov_chain import MarkovChain
from markov_solver.core.model.markov_link import MarkovLink
from markov_solver.core.model.markov_state import MarkovState


def create_chain_from_file(path):
    with open(path, "r") as definition_file:
        definition = yaml.load(definition_file, Loader=yaml.FullLoader)

    mc = MarkovChain()

    if "symbols" in definition:
        mc.add_symbols(**definition["symbols"])

    for edge in definition["chain"]:
        head = MarkovState(edge["from"])
        tail = MarkovState(edge["to"])
        link = MarkovLink(head, tail, edge["value"])
        mc.add_state(head)
        mc.add_state(tail)
        mc.add_link(link)

    return mc
