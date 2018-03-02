from data import Value, MAX_INT

MAX_MEM = MAX_INT

class Core(object):
    def __init__(self, initAx=Value(None)):
        self.ax = initAx  # Accumulator
        self.pc = 0  # Program Counter

    def __del__(self):
        pass

class VM(object):
    def __init__(self, istream=[], dynamicMem=False, initMem=None):
        self.core = Core()
        self.mem = [Value(None)] * memSize  # Memory
        self.dynamicMem = dynamicMem
        self.istream = [Value(i) for i in istream]  # For safety
        self.ostream = []
        self.cmd = None  # Instruction list

    def setMem(self, index, value):
        try:
            self.mem[index] = value
        except TypeError:
            raise TypeError("Index must be integer")
        except IndexError as e:
            if not (self.dynamicMem and 0 <= index <= MAX_MEM):
                raise IndexError("That's not a valid place")
            self.mem += [None] * (index - len(self.mem) - 1) + [value]

    def getMem(self, index):
        try:
            return self.mem[index]
        except TypeError:
            raise TypeError("Index must be integer")
        except IndexError:
            raise IndexError("That's not a valid place")

    # This seems unnecessary now but it may be potentially useful later
    def runCmd(self, cmdFunc, *cmdArgs):
        return cmdFunc(self, *cmdArgs)
