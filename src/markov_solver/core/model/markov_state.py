class MarkovState:
    def __init__(self, value):
        self.value = value

    def pretty_str(self):
        if isinstance(self.value, str):
            return self.value
        string = ""
        sym = "A"
        idx = 0
        for i in self.value:
            string += "{}{}".format(chr(ord(sym) + idx), i)
            idx += 1
        return string

    def __str__(self):
        return "{}".format(self.value)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if not isinstance(other, MarkovState):
            return False
        return self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, MarkovState):
            return False
        return self.value < other.value

    def __getitem__(self, item):
        return self.value
