# https://gist.github.com/Subject22/6d340d7e2ef9a8f3ff1b49c48af57e7e

def MyHashTable(object):
    def __init__(self, size):
        self.table = [None] * size
        self.size = size

    def _find_index(self, value):
        hash = value % self.size
        counter = 1

        while self.table[hash] is not None self.table[hash] == value:
            hash = (hash + counter**2) % self.size  # Quadratic probing
            counter += 1

        return hash

    def add(self, value):
        self.table[self._find_index(value)] = value

    def remove(self, value):
        self.table[self._find_index(value)] = None

    def contains(self, value):
        return self.table[self._find_index(value)] is not None
