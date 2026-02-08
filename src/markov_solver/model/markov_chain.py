from typing import Any, Dict, List, Optional, Set, Tuple, Union

import sympy  # type: ignore
from graphviz import Digraph  # type: ignore

from markov_solver.model.markov_link import MarkovLink
from markov_solver.model.markov_state import MarkovState

FLOATING_POINT_PRECISION = 12


class MarkovChain:
    def __init__(self) -> None:
        self.states: Set[MarkovState] = set()
        self.links: Set[MarkovLink] = set()
        self.symbols: Dict[str, float] = dict()

    def add_state(self, value: Union[MarkovState, Any]) -> MarkovState:
        state = value if isinstance(value, MarkovState) else MarkovState(value)
        self.states.add(state)
        return state

    def add_link(self, link: MarkovLink) -> bool:
        if link not in self.links:
            self.links.add(link)
            return True
        return False

    def add_symbols(self, **kwargs: float) -> None:
        for symbol, value in kwargs.items():
            self.symbols[symbol] = value

    def in_links(self, state: MarkovState) -> List[MarkovLink]:
        return list(link for link in self.links if link.head == state)

    def out_links(self, state: MarkovState) -> List[MarkovLink]:
        return list(link for link in self.links if link.tail == state)

    def find_link(
        self, state1: MarkovState, state2: MarkovState
    ) -> Optional[MarkovLink]:
        return next(
            (link for link in self.out_links(state1) if link.head == state2), None
        )

    def get_states(self) -> List[MarkovState]:
        return sorted(self.states)

    def transition_matrix(self, evaluate: bool = False) -> List[List[Any]]:
        states = sorted(self.get_states())
        tmatrix: List[List[Any]] = []
        for state1 in states:
            row: List[Any] = []
            normalization_factor: Optional[str] = None
            for state2 in states:
                link = self.find_link(state1, state2)
                link_value: Any = 0.0 if link is None else link.value
                row.append(link_value)
                if link_value != 0.0:
                    normalization_factor = "+".join(
                        filter(None, (normalization_factor, link_value))
                    )
            for i in range(len(row)):
                if row[i] != 0.0:
                    row[i] = "({})/({})".format(row[i], normalization_factor)
            tmatrix.append(row)
        if evaluate is True:
            for r in range(len(tmatrix)):
                for c in range(len(tmatrix[r])):
                    tmatrix[r][c] = self.__evaluate_factor(tmatrix[r][c])
        return tmatrix

    def solve(self) -> Dict[str, Any]:
        """
        Solves a Markov Chain.
        :return: the solutions of the Markov Chain.
        """
        equations, variables = self.generate_sympy_equations()
        solutions = sympy.solve(equations, variables)

        state_solutions: Dict[str, Any] = {}
        for symbol, value in solutions.items():
            state_solutions[symbol.name] = value

        return state_solutions

    def generate_sympy_equations(self) -> Tuple[List[Any], Set[Any]]:
        """
        Generate sympy flow equations from the Markov chain.
        :return: the list of equations
        """
        variables: Set[Any] = set()
        equations: List[Any] = []
        for eqn in self.generate_equations():
            equation: Any = 0
            lhs = eqn[0]
            rhs = eqn[1]
            for lhs_link in lhs:
                variable = sympy.Symbol(lhs_link.tail.pretty_str())
                variables.add(variable)
                link_value = self.__evaluate_factor(lhs_link.value)
                equation += variable * link_value

            for rhs_link in rhs:
                variable = sympy.Symbol(rhs_link.tail.pretty_str())
                variables.add(variable)
                link_value = self.__evaluate_factor(rhs_link.value)
                equation -= variable * link_value

            equations.append(equation)

        equation = -1
        for variable in variables:
            equation += variable
        equations.append(equation)

        return equations, variables

    def generate_equations(self) -> List[Tuple[List[MarkovLink], List[MarkovLink]]]:
        """
        Generate flow equations from the Markov chain.
        :return: the list of equations.
        """
        equations: List[Tuple[List[MarkovLink], List[MarkovLink]]] = []
        for s in sorted(self.states):
            lhs = self.out_links(s)
            rhs = self.in_links(s)
            equations.append((lhs, rhs))

        return equations

    def matrixs(self) -> str:
        """
        Return the string representation of the matrix.
        :return: the string representation.
        """
        s = ""
        for r in self.transition_matrix():
            s += "{}\n".format(",".join(map(str, r)))
        return s

    def render_graph(
        self, filename: str = "out/MarkovChain", format: str = "svg"
    ) -> None:
        graph = Digraph(engine="dot")
        graph.attr(rankdir="LR")

        for state in sorted(self.states):
            graph.node(str(state))
            # graph.node(str(state), pos="{},{}!".format(int(state.value[0]) * 2, -int(state.value[1]) * 2))

        for link in self.links:
            graph.edge(str(link.tail), str(link.head), str(link.value))

        graph.render(filename=filename, format=format)

    def __evaluate_factor(self, factor: Any) -> float:
        if isinstance(factor, int) or isinstance(factor, float):
            return float(factor)
        value = factor
        for k, v in self.symbols.items():
            value = value.replace(k, str(v))
        return float(round(eval(value), FLOATING_POINT_PRECISION))

    def __str__(self) -> str:
        return "States: {}\nLinks: {}\nSymbols: {}\n".format(
            sorted(self.states), sorted(self.links), self.symbols
        )

    def __repr__(self) -> str:
        return self.__str__()


if __name__ == "__main__":
    markov_chain = MarkovChain()

    s_0_0 = MarkovState((0, 0))  # Bull Market
    s_0_1 = MarkovState((0, 1))  # Bear Market
    s_1_0 = MarkovState((1, 0))  # Stagnant Market

    markov_chain.add_state(s_0_0)
    markov_chain.add_state(s_0_1)
    markov_chain.add_state(s_1_0)

    markov_chain.add_symbols(p=0.9, q=0.8, r=0.5)

    markov_chain.add_link(MarkovLink(s_0_0, s_0_0, "p"))
    markov_chain.add_link(MarkovLink(s_0_0, s_0_1, "(1-p)*0.75"))
    markov_chain.add_link(MarkovLink(s_0_0, s_1_0, "(1-p)*0.25"))

    markov_chain.add_link(MarkovLink(s_0_1, s_0_1, "q"))
    markov_chain.add_link(MarkovLink(s_0_1, s_0_0, "(1-q)*0.75"))
    markov_chain.add_link(MarkovLink(s_0_1, s_1_0, "(1-q)*0.25"))

    markov_chain.add_link(MarkovLink(s_1_0, s_1_0, "r"))
    markov_chain.add_link(MarkovLink(s_1_0, s_0_0, "(1-r)*0.5"))
    markov_chain.add_link(MarkovLink(s_1_0, s_0_1, "(1-r)*0.5"))

    print(markov_chain)

    markov_chain.render_graph()

    for s in markov_chain.states:
        print(s.pretty_str())

    print(markov_chain.transition_matrix())
    print(markov_chain.transition_matrix(evaluate=True))
    print(markov_chain.matrixs())

    eqn_string = ""
    for equation in markov_chain.generate_equations():
        lhs = equation[0]
        rhs = equation[1]
        for factor in lhs:
            eqn_string += "{}*{}+".format(factor.value, factor.head)
        eqn_string += "="
        for factor in rhs:
            eqn_string += "{}*{}+".format(factor.value, factor.tail)
        eqn_string += "\n"
    print(eqn_string)

    for eqn in markov_chain.generate_sympy_equations():
        print(eqn)

    solutions = markov_chain.solve()
    for k, v in sorted(solutions.items()):
        print("{}={}".format(k, v))
