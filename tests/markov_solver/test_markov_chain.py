from assertpy import assert_that

from markov_solver.core.model.markov_chain import MarkovChain
from markov_solver.core.model.markov_link import MarkovLink
from markov_solver.core.model.markov_state import MarkovState


class TestMarkovChain:
    def test_init(self) -> None:
        chain = MarkovChain()
        assert_that(chain.states).is_empty()
        assert_that(chain.links).is_empty()
        assert_that(chain.symbols).is_empty()

    def test_add_state_with_value(self) -> None:
        chain = MarkovChain()
        state = chain.add_state("Sunny")
        assert_that(state.value).is_equal_to("Sunny")
        assert_that(chain.states).contains(state)

    def test_add_state_with_markov_state(self) -> None:
        chain = MarkovChain()
        state = MarkovState("Sunny")
        result = chain.add_state(state)
        assert_that(result).is_equal_to(state)
        assert_that(chain.states).contains(state)

    def test_add_link(self) -> None:
        chain = MarkovChain()
        s1 = chain.add_state("A")
        s2 = chain.add_state("B")
        link = MarkovLink(s1, s2, 0.5)
        result = chain.add_link(link)
        assert_that(result).is_true()
        assert_that(chain.links).contains(link)

    def test_add_link_duplicate(self) -> None:
        chain = MarkovChain()
        s1 = chain.add_state("A")
        s2 = chain.add_state("B")
        link = MarkovLink(s1, s2, 0.5)
        chain.add_link(link)
        result = chain.add_link(link)
        assert_that(result).is_false()

    def test_add_symbols(self) -> None:
        chain = MarkovChain()
        chain.add_symbols(p=0.9, q=0.8)
        assert_that(chain.symbols).is_equal_to({"p": 0.9, "q": 0.8})

    def test_in_links(self) -> None:
        chain = MarkovChain()
        s1 = chain.add_state("A")
        s2 = chain.add_state("B")
        link = MarkovLink(s1, s2, 0.5)
        chain.add_link(link)
        in_links = chain.in_links(s2)
        assert_that(in_links).contains(link)

    def test_out_links(self) -> None:
        chain = MarkovChain()
        s1 = chain.add_state("A")
        s2 = chain.add_state("B")
        link = MarkovLink(s1, s2, 0.5)
        chain.add_link(link)
        out_links = chain.out_links(s1)
        assert_that(out_links).contains(link)

    def test_find_link_exists(self) -> None:
        chain = MarkovChain()
        s1 = chain.add_state("A")
        s2 = chain.add_state("B")
        link = MarkovLink(s1, s2, 0.5)
        chain.add_link(link)
        found = chain.find_link(s1, s2)
        assert_that(found).is_equal_to(link)

    def test_find_link_not_exists(self) -> None:
        chain = MarkovChain()
        s1 = chain.add_state("A")
        s2 = chain.add_state("B")
        found = chain.find_link(s1, s2)
        assert_that(found).is_none()

    def test_get_states(self) -> None:
        chain = MarkovChain()
        chain.add_state("B")
        chain.add_state("A")
        states = chain.get_states()
        assert_that(states[0].value).is_equal_to("A")
        assert_that(states[1].value).is_equal_to("B")

    def test_transition_matrix(self) -> None:
        chain = MarkovChain()
        s1 = chain.add_state("A")
        s2 = chain.add_state("B")
        chain.add_link(MarkovLink(s1, s1, "0.7"))
        chain.add_link(MarkovLink(s1, s2, "0.3"))
        chain.add_link(MarkovLink(s2, s1, "0.4"))
        chain.add_link(MarkovLink(s2, s2, "0.6"))
        matrix = chain.transition_matrix()
        assert_that(len(matrix)).is_equal_to(2)

    def test_transition_matrix_evaluate(self) -> None:
        chain = MarkovChain()
        s1 = chain.add_state("A")
        s2 = chain.add_state("B")
        chain.add_link(MarkovLink(s1, s1, "0.7"))
        chain.add_link(MarkovLink(s1, s2, "0.3"))
        chain.add_link(MarkovLink(s2, s1, "0.4"))
        chain.add_link(MarkovLink(s2, s2, "0.6"))
        matrix = chain.transition_matrix(evaluate=True)
        assert_that(matrix[0][0]).is_equal_to(0.7)
        assert_that(matrix[0][1]).is_equal_to(0.3)

    def test_solve(self) -> None:
        chain = MarkovChain()
        sunny = chain.add_state("Sunny")
        rainy = chain.add_state("Rainy")
        chain.add_link(MarkovLink(sunny, sunny, 0.9))
        chain.add_link(MarkovLink(sunny, rainy, 0.1))
        chain.add_link(MarkovLink(rainy, sunny, 0.5))
        chain.add_link(MarkovLink(rainy, rainy, 0.5))
        solutions = chain.solve()
        assert_that(solutions).contains_key("Sunny")
        assert_that(solutions).contains_key("Rainy")

    def test_generate_equations(self) -> None:
        chain = MarkovChain()
        s1 = chain.add_state("A")
        s2 = chain.add_state("B")
        chain.add_link(MarkovLink(s1, s2, 0.5))
        equations = chain.generate_equations()
        assert_that(len(equations)).is_equal_to(2)

    def test_matrixs(self) -> None:
        chain = MarkovChain()
        s1 = chain.add_state("A")
        s2 = chain.add_state("B")
        chain.add_link(MarkovLink(s1, s1, "0.7"))
        chain.add_link(MarkovLink(s1, s2, "0.3"))
        chain.add_link(MarkovLink(s2, s1, "0.4"))
        chain.add_link(MarkovLink(s2, s2, "0.6"))
        result = chain.matrixs()
        assert_that(result).contains(",")

    def test_render_graph(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        chain = MarkovChain()
        s1 = chain.add_state("A")
        s2 = chain.add_state("B")
        chain.add_link(MarkovLink(s1, s2, 0.5))
        output_file = tmp_path / "graph"
        chain.render_graph(str(output_file), "svg")
        assert_that((tmp_path / "graph.svg").exists()).is_true()

    def test_str(self) -> None:
        chain = MarkovChain()
        chain.add_state("A")
        chain.add_symbols(p=0.5)
        result = str(chain)
        assert_that(result).contains("States:")
        assert_that(result).contains("Links:")
        assert_that(result).contains("Symbols:")

    def test_repr(self) -> None:
        chain = MarkovChain()
        chain.add_state("A")
        assert_that(repr(chain)).is_equal_to(str(chain))

    def test_solve_with_symbols(self) -> None:
        chain = MarkovChain()
        s1 = chain.add_state("A")
        s2 = chain.add_state("B")
        chain.add_symbols(p=0.9)
        chain.add_link(MarkovLink(s1, s1, "p"))
        chain.add_link(MarkovLink(s1, s2, "1-p"))
        chain.add_link(MarkovLink(s2, s1, 0.5))
        chain.add_link(MarkovLink(s2, s2, 0.5))
        solutions = chain.solve()
        assert_that(solutions).is_not_empty()
