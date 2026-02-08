from assertpy import assert_that

from markov_solver.model.markov_state import MarkovState


class TestMarkovState:
    def test_init_with_string(self) -> None:
        state = MarkovState("Sunny")
        assert_that(state.value).is_equal_to("Sunny")

    def test_init_with_tuple(self) -> None:
        state = MarkovState((0, 1))
        assert_that(state.value).is_equal_to((0, 1))

    def test_pretty_str_with_string(self) -> None:
        state = MarkovState("Sunny")
        assert_that(state.pretty_str()).is_equal_to("Sunny")

    def test_pretty_str_with_tuple(self) -> None:
        state = MarkovState((0, 1))
        assert_that(state.pretty_str()).is_equal_to("A0B1")

    def test_pretty_str_with_longer_tuple(self) -> None:
        state = MarkovState((1, 2, 3))
        assert_that(state.pretty_str()).is_equal_to("A1B2C3")

    def test_str(self) -> None:
        state = MarkovState("Sunny")
        assert_that(str(state)).is_equal_to("Sunny")

    def test_repr(self) -> None:
        state = MarkovState("Sunny")
        assert_that(repr(state)).is_equal_to("Sunny")

    def test_hash(self) -> None:
        state1 = MarkovState("Sunny")
        state2 = MarkovState("Sunny")
        assert_that(hash(state1)).is_equal_to(hash(state2))

    def test_eq_same_value(self) -> None:
        state1 = MarkovState("Sunny")
        state2 = MarkovState("Sunny")
        assert_that(state1).is_equal_to(state2)

    def test_eq_different_value(self) -> None:
        state1 = MarkovState("Sunny")
        state2 = MarkovState("Rainy")
        assert_that(state1).is_not_equal_to(state2)

    def test_eq_non_markov_state(self) -> None:
        state = MarkovState("Sunny")
        assert_that(state.__eq__("Sunny")).is_false()

    def test_ne_same_value(self) -> None:
        state1 = MarkovState("Sunny")
        state2 = MarkovState("Sunny")
        assert_that(state1 != state2).is_false()

    def test_ne_different_value(self) -> None:
        state1 = MarkovState("Sunny")
        state2 = MarkovState("Rainy")
        assert_that(state1 != state2).is_true()

    def test_ne_non_markov_state(self) -> None:
        state = MarkovState("Sunny")
        assert_that(state.__ne__("Sunny")).is_false()

    def test_ge(self) -> None:
        state1 = MarkovState("Sunny")
        state2 = MarkovState("Rainy")
        assert_that(state1 >= state2).is_true()
        assert_that(state1 >= state1).is_true()

    def test_ge_non_markov_state(self) -> None:
        state = MarkovState("Sunny")
        assert_that(state.__ge__("Sunny")).is_false()

    def test_gt(self) -> None:
        state1 = MarkovState("Sunny")
        state2 = MarkovState("Rainy")
        assert_that(state1 > state2).is_true()
        assert_that(state1 > state1).is_false()

    def test_gt_non_markov_state(self) -> None:
        state = MarkovState("Sunny")
        assert_that(state.__gt__("Sunny")).is_false()

    def test_le(self) -> None:
        state1 = MarkovState("Rainy")
        state2 = MarkovState("Sunny")
        assert_that(state1 <= state2).is_true()
        assert_that(state1 <= state1).is_true()

    def test_le_non_markov_state(self) -> None:
        state = MarkovState("Sunny")
        assert_that(state.__le__("Sunny")).is_false()

    def test_lt(self) -> None:
        state1 = MarkovState("Rainy")
        state2 = MarkovState("Sunny")
        assert_that(state1 < state2).is_true()
        assert_that(state1 < state1).is_false()

    def test_lt_non_markov_state(self) -> None:
        state = MarkovState("Sunny")
        assert_that(state.__lt__("Sunny")).is_false()

    def test_getitem(self) -> None:
        state = MarkovState("Sunny")
        assert_that(state[0]).is_equal_to("Sunny")

    def test_sorting(self) -> None:
        states = [MarkovState("C"), MarkovState("A"), MarkovState("B")]
        sorted_states = sorted(states)
        assert_that(sorted_states[0].value).is_equal_to("A")
        assert_that(sorted_states[1].value).is_equal_to("B")
        assert_that(sorted_states[2].value).is_equal_to("C")
