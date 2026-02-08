from typing import Any, Tuple, Union


class MarkovState:
    def __init__(self, value: Union[str, Tuple[int, ...]]) -> None:
        self.value = value

    def pretty_str(self) -> str:
        if isinstance(self.value, str):
            return self.value
        string = ""
        sym = "A"
        idx = 0
        for i in self.value:
            string += "{}{}".format(chr(ord(sym) + idx), i)
            idx += 1
        return string

    def __str__(self) -> str:
        return "{}".format(self.value)

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MarkovState):
            return False
        return self.value == other.value

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, MarkovState):
            return False
        return self.value != other.value

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, MarkovState):
            return False
        return str(self.value) >= str(other.value)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, MarkovState):
            return False
        return str(self.value) > str(other.value)

    def __le__(self, other: object) -> bool:
        if not isinstance(other, MarkovState):
            return False
        return str(self.value) <= str(other.value)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, MarkovState):
            return False
        return str(self.value) < str(other.value)

    def __getitem__(self, item: Any) -> Union[str, Tuple[int, ...]]:
        return self.value
