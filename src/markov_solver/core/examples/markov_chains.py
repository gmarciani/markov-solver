from markov_solver.core.model.markov_chain import MarkovChain
from markov_solver.core.model.markov_link import MarkovLink


class MarkovChainAlgorithm1(MarkovChain):
    def __init__(self, N, l1, l2, m1, m2):
        """
        Generate the Markov Chain for Algorithm 1.
        :param N: (int) the number of Cloudlet servers.
        :param l1: (float) the arrival rate for tasks of type 1.
        :param l2: (float) the arrival rate for tasks of type 2.
        :param m1: (float) the service rate for tasks of type 1.
        :param m2: (float) the service rate for tasks of type 2.
        """
        super().__init__()
        self.add_symbols(l1=l1, l2=l2, l=l1 + l2, m1=m1, m2=m2)
        self.__generate_markov_chain(N, l1, l2, m1, m2)

    def __generate_markov_chain(self, N, l1, l2, m1, m2):
        """
        Generate the matrix for the flow equations.
        :param N: (int) the number of Cloudlet servers.
        :param l1: (float) the arrival rate for tasks of type 1.
        :param l2: (float) the arrival rate for tasks of type 2.
        :param m1: (float) the service rate for tasks of type 1.
        :param m2: (float) the service rate for tasks of type 2.
        """
        state = self.add_state((0, 0))
        self.__explore_state(state, N, l1, l2, m1, m2)

    def __explore_state(self, state, N, l1, l2, m1, m2):
        """
        Recursive state exploration.
        :param state: the current state.
        :param N: (int) the number of Cloudlet servers.
        :param l1: (float) the arrival rate for tasks of type 1.
        :param l2: (float) the arrival rate for tasks of type 2.
        :param m1: (float) the service rate for tasks of type 1.
        :param m2: (float) the service rate for tasks of type 2.
        """
        n1 = state.value[0]
        n2 = state.value[1]

        if n1 + n2 < N:  # SUBMIT_TO_CLOUDLET
            # arrival task 1
            state_arrival = self.add_state((n1 + 1, n2))
            link = MarkovLink(state, state_arrival, "l1")
            added = self.add_link(link)
            if added:
                self.__explore_state(state_arrival, N, l1, l2, m1, m2)

            # arrival task 2
            state_arrival = self.add_state((n1, n2 + 1))
            link = MarkovLink(state, state_arrival, "l2")
            added = self.add_link(link)
            if added:
                self.__explore_state(state_arrival, N, l1, l2, m1, m2)

        elif n1 + n2 == N:  # SUBMIT_TO_CLOUD
            # arrival task 1 or task 2
            state_arrival = state
            link = MarkovLink(state, state_arrival, "l")
            self.add_link(link)

        else:
            raise ValueError("Encountered an invalid state: {}. n1+n2 must be <= N ({})".format(state, N))

        if n1 > 0:
            # service task 1
            state_served = self.add_state((n1 - 1, n2))
            link = MarkovLink(state, state_served, "{}*m1".format(n1))
            added = self.add_link(link)
            if added:
                self.__explore_state(state_served, N, l1, l2, m1, m2)

        if n2 > 0:
            # service task 2
            state_served = self.add_state((n1, n2 - 1))
            link = MarkovLink(state, state_served, "{}*m2".format(n2))
            added = self.add_link(link)
            if added:
                self.__explore_state(state_served, N, l1, l2, m1, m2)


class MarkovChainAlgorithm2(MarkovChain):
    def __init__(self, N, S, l1, l2, m1, m2):
        """
        Generate the Markov Chain for Algorithm 2.
        :param N: (int) the number of Cloudlet servers.
        :param S: (int) the Cloudlet threshold.
        :param l1: (float) the arrival rate for tasks of type 1.
        :param l2: (float) the arrival rate for tasks of type 2.
        :param m1: (float) the service rate for tasks of type 1.
        :param m2: (float) the service rate for tasks of type 2.
        """
        super().__init__()
        self.add_symbols(l1=l1, l2=l2, l=l1 + l2, m1=m1, m2=m2)
        self.__generate_markov_chain(N, S, l1, l2, m1, m2)

    def __generate_markov_chain(self, N, S, l1, l2, m1, m2):
        """
        Generate the matrix for the flow equations.
        :param N: (int) the number of Cloudlet servers.
        :param S: (int) the Cloudlet threshold.
        :param l1: (float) the arrival rate for tasks of type 1.
        :param l2: (float) the arrival rate for tasks of type 2.
        :param m1: (float) the service rate for tasks of type 1.
        :param m2: (float) the service rate for tasks of type 2.
        """
        state = self.add_state((0, 0))
        self.__explore_state(state, N, S, l1, l2, m1, m2)

    def __explore_state(self, state, N, S, l1, l2, m1, m2):
        """
        Recursive state exploration.
        :param state: the current state.
        :param N: (int) the number of Cloudlet servers.
        :param S: (int) the Cloudlet threshold.
        :param l1: (float) the arrival rate for tasks of type 1.
        :param l2: (float) the arrival rate for tasks of type 2.
        :param m1: (float) the service rate for tasks of type 1.
        :param m2: (float) the service rate for tasks of type 2.
        """
        n1 = state.value[0]
        n2 = state.value[1]

        if n1 == N:  # SUBMIT_TO_CLOUD
            # arrival task 1 or task 2
            state_arrival = state
            link = MarkovLink(state, state_arrival, "l")
            self.add_link(link)

        elif n1 + n2 < S:  # SUBMIT_TO_CLOUDLET
            # arrival task 1
            state_arrival = self.add_state((n1 + 1, n2))
            link = MarkovLink(state, state_arrival, "l1")
            added = self.add_link(link)
            if added:
                self.__explore_state(state_arrival, N, S, l1, l2, m1, m2)

            # arrival task 2
            state_arrival = self.add_state((n1, n2 + 1))
            link = MarkovLink(state, state_arrival, "l2")
            added = self.add_link(link)
            if added:
                self.__explore_state(state_arrival, N, S, l1, l2, m1, m2)

        elif n2 > 0:  # SUBMIT_TO_CLOUDLET_WITH_INTERRUPTION
            # arrival task 1 + interruption task 2
            state_arrival = self.add_state((n1 + 1, n2 - 1))
            link = MarkovLink(state, state_arrival, "l1")
            added = self.add_link(link)
            if added:
                self.__explore_state(state_arrival, N, S, l1, l2, m1, m2)

            # arrival task 2
            state_arrival = state
            link = MarkovLink(state, state_arrival, "l2")
            self.add_link(link)

        elif n1 + n2 >= S and n2 == 0:  # SUBMIT TO CLOUDLET ONLY TASK 1
            # arrival task 1
            state_arrival = self.add_state((n1 + 1, n2))
            link = MarkovLink(state, state_arrival, "l1")
            added = self.add_link(link)
            if added:
                self.__explore_state(state_arrival, N, S, l1, l2, m1, m2)

            # arrival task 2
            state_arrival = state
            link = MarkovLink(state, state_arrival, "l2")
            self.add_link(link)

        else:
            raise ValueError(
                "Encountered an invalid state: {}. n1+n2 must be <= N ({}) and n2 must be <= S ({}).".format(
                    state, N, S
                )
            )

        if n1 > 0:
            # service task 1
            state_served = self.add_state((n1 - 1, n2))
            link = MarkovLink(state, state_served, "{}*m1".format(n1))
            added = self.add_link(link)
            if added:
                self.__explore_state(state_served, N, S, l1, l2, m1, m2)

        if n2 > 0:
            # service task 2
            state_served = self.add_state((n1, n2 - 1))
            link = MarkovLink(state, state_served, "{}*m2".format(n2))
            added = self.add_link(link)
            if added:
                self.__explore_state(state_served, N, S, l1, l2, m1, m2)


if __name__ == "__main__":
    N = 2
    S = 1
    l1 = 6
    l2 = 6.25
    m1 = 0.45
    m2 = 0.25

    print("MARKOV CHAIN: ALGORITHM 1")

    markov_chain = MarkovChainAlgorithm1(N, l1, l2, m1, m2)
    print(markov_chain)
    print(markov_chain.transition_matrix())
    markov_chain.render_graph("out/MarkovChainAlgorithm1")

    solutions = markov_chain.solve()
    for k, v in sorted(solutions.items()):
        print("{}={}".format(k, v))

    print("MARKOV CHAIN: ALGORITHM 2")

    markov_chain = MarkovChainAlgorithm2(N, S, l1, l2, m1, m2)
    print(markov_chain)
    print(markov_chain.transition_matrix())
    markov_chain.render_graph("out/MarkovChainAlgorithm2")

    solutions = markov_chain.solve()
    for k, v in sorted(solutions.items()):
        print("{}={}".format(k, v))
