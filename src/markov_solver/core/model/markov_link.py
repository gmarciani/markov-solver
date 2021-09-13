class MarkovLink:
    def __init__(self, tail, head, value):
        self.tail = tail
        self.head = head
        self.value = value

    def __str__(self):
        return "({}-{{{}}}->{})".format(self.tail, self.value, self.head)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if not isinstance(other, MarkovLink):
            return False
        return self.tail == other.tail and self.head == other.head and self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, MarkovLink):
            return False
        if self.tail == other.tail:
            return self.head < other.head
        return self.tail < other.tail
