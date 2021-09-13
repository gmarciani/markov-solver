from markov_solver.core.examples.markov_chains import MarkovChainAlgorithm1


def create_chain_from_file(path):
    N = 2
    S = 1
    l1 = 6
    l2 = 6.25
    m1 = 0.45
    m2 = 0.25

    return MarkovChainAlgorithm1(N, l1, l2, m1, m2)
