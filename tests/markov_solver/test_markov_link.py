from assertpy import assert_that

from markov_solver.core.model.markov_link import MarkovLink
from markov_solver.core.model.markov_state import MarkovState


class TestMarkovLink:
    def test_init(self) -> None:
        tail = MarkovState("A")
        head = MarkovState("B")
        link = MarkovLink(tail, head, 0.5)
        assert_that(link.tail).is_equal_to(tail)
        assert_that(link.head).is_equal_to(head)
        assert_that(link.value).is_equal_to(0.5)

    def test_init_with_string_value(self) -> None:
        tail = MarkovState("A")
        head = MarkovState("B")
        link = MarkovLink(tail, head, "p")
        assert_that(link.value).is_equal_to("p")

    def test_str(self) -> None:
        tail = MarkovState("A")
        head = MarkovState("B")
        link = MarkovLink(tail, head, 0.5)
        assert_that(str(link)).is_equal_to("(A-{0.5}->B)")

    def test_repr(self) -> None:
        tail = MarkovState("A")
        head = MarkovState("B")
        link = MarkovLink(tail, head, 0.5)
        assert_that(repr(link)).is_equal_to("(A-{0.5}->B)")

    def test_hash(self) -> None:
        tail = MarkovState("A")
        head = MarkovState("B")
        link1 = MarkovLink(tail, head, 0.5)
        link2 = MarkovLink(tail, head, 0.5)
        assert_that(hash(link1)).is_equal_to(hash(link2))

    def test_eq_same(self) -> None:
        tail = MarkovState("A")
        head = MarkovState("B")
        link1 = MarkovLink(tail, head, 0.5)
        link2 = MarkovLink(tail, head, 0.5)
        assert_that(link1).is_equal_to(link2)

    def test_eq_different_tail(self) -> None:
        head = MarkovState("B")
        link1 = MarkovLink(MarkovState("A"), head, 0.5)
        link2 = MarkovLink(MarkovState("C"), head, 0.5)
        assert_that(link1).is_not_equal_to(link2)

    def test_eq_non_markov_link(self) -> None:
        link = MarkovLink(MarkovState("A"), MarkovState("B"), 0.5)
        assert_that(link.__eq__("not a link")).is_false()

    def test_ne_same(self) -> None:
        tail = MarkovState("A")
        head = MarkovState("B")
        link1 = MarkovLink(tail, head, 0.5)
        link2 = MarkovLink(tail, head, 0.5)
        assert_that(link1 != link2).is_false()

    def test_ne_different(self) -> None:
        tail = MarkovState("A")
        head = MarkovState("B")
        link1 = MarkovLink(tail, head, 0.5)
        link2 = MarkovLink(tail, head, 0.7)
        assert_that(link1 != link2).is_true()

    def test_ne_non_markov_link(self) -> None:
        link = MarkovLink(MarkovState("A"), MarkovState("B"), 0.5)
        assert_that(link.__ne__("not a link")).is_false()

    def test_ge_same_tail(self) -> None:
        tail = MarkovState("A")
        link1 = MarkovLink(tail, MarkovState("C"), 0.5)
        link2 = MarkovLink(tail, MarkovState("B"), 0.5)
        assert_that(link1 >= link2).is_true()

    def test_ge_different_tail(self) -> None:
        link1 = MarkovLink(MarkovState("B"), MarkovState("X"), 0.5)
        link2 = MarkovLink(MarkovState("A"), MarkovState("X"), 0.5)
        assert_that(link1 >= link2).is_true()

    def test_ge_non_markov_link(self) -> None:
        link = MarkovLink(MarkovState("A"), MarkovState("B"), 0.5)
        assert_that(link.__ge__("not a link")).is_false()

    def test_gt_same_tail(self) -> None:
        tail = MarkovState("A")
        link1 = MarkovLink(tail, MarkovState("C"), 0.5)
        link2 = MarkovLink(tail, MarkovState("B"), 0.5)
        assert_that(link1 > link2).is_true()

    def test_gt_different_tail(self) -> None:
        link1 = MarkovLink(MarkovState("B"), MarkovState("X"), 0.5)
        link2 = MarkovLink(MarkovState("A"), MarkovState("X"), 0.5)
        assert_that(link1 > link2).is_true()

    def test_gt_non_markov_link(self) -> None:
        link = MarkovLink(MarkovState("A"), MarkovState("B"), 0.5)
        assert_that(link.__gt__("not a link")).is_false()

    def test_le_same_tail(self) -> None:
        tail = MarkovState("A")
        link1 = MarkovLink(tail, MarkovState("B"), 0.5)
        link2 = MarkovLink(tail, MarkovState("C"), 0.5)
        assert_that(link1 <= link2).is_true()

    def test_le_different_tail(self) -> None:
        link1 = MarkovLink(MarkovState("A"), MarkovState("X"), 0.5)
        link2 = MarkovLink(MarkovState("B"), MarkovState("X"), 0.5)
        assert_that(link1 <= link2).is_true()

    def test_le_non_markov_link(self) -> None:
        link = MarkovLink(MarkovState("A"), MarkovState("B"), 0.5)
        assert_that(link.__le__("not a link")).is_false()

    def test_lt_same_tail(self) -> None:
        tail = MarkovState("A")
        link1 = MarkovLink(tail, MarkovState("B"), 0.5)
        link2 = MarkovLink(tail, MarkovState("C"), 0.5)
        assert_that(link1 < link2).is_true()

    def test_lt_different_tail(self) -> None:
        link1 = MarkovLink(MarkovState("A"), MarkovState("X"), 0.5)
        link2 = MarkovLink(MarkovState("B"), MarkovState("X"), 0.5)
        assert_that(link1 < link2).is_true()

    def test_lt_non_markov_link(self) -> None:
        link = MarkovLink(MarkovState("A"), MarkovState("B"), 0.5)
        assert_that(link.__lt__("not a link")).is_false()
