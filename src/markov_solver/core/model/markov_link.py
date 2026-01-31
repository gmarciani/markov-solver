from typing import Union

from markov_solver.core.model.markov_state import MarkovState


class MarkovLink:
    def __init__(
        self, tail: MarkovState, head: MarkovState, value: Union[str, float]
    ) -> None:
        self.tail = tail
        self.head = head
        self.value = value

    def __str__(self) -> str:
        return "({}-{{{}}}->{})".format(self.tail, self.value, self.head)

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MarkovLink):
            return False
        return (
            self.tail == other.tail
            and self.head == other.head
            and self.value == other.value
        )

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, MarkovLink):
            return False
        return (
            self.tail != other.tail
            or self.head != other.head
            or self.value != other.value
        )

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, MarkovLink):
            return False
        if self.tail == other.tail:
            return self.head >= other.head
        return self.tail >= other.tail

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, MarkovLink):
            return False
        if self.tail == other.tail:
            return self.head > other.head
        return self.tail > other.tail

    def __le__(self, other: object) -> bool:
        if not isinstance(other, MarkovLink):
            return False
        if self.tail == other.tail:
            return self.head <= other.head
        return self.tail <= other.tail

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, MarkovLink):
            return False
        if self.tail == other.tail:
            return self.head < other.head
        return self.tail < other.tail
