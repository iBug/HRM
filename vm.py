MAX_MEM = 999

class VM(object):
    def __init__(self, memSize=16):
        self.mem = [None] * memSize  # Memory
        self.ax = None  # Accumulator
        self.dynamicMem = False

    def setMem(self, index, value):
        if not is_instance(index, int):
            raise TypeError("index is not integer!")

        try:
            self.mem[index] = value
        except IndexError as e:
            if not self.dynamicMem:
                raise
            if index < 0 or index > MAX_MEM:
                raise IndexError("That's not a valid place")
            self.mem += [None] * (index - len(self.mem) - 1) + [value]

    def __del__(self):
        pass

