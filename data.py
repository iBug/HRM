MAX_INT = 999
MIN_INT = -999

class Command(object):
    def __init__(self, cmd, *ops):
        self.cmd = cmd  # Command
        self.ops = ops  # Operands

class Value(object):

    NONE = 0
    LETTER = 1
    NUMBER = 2

    def __init__(self, v=None):
        if is_instance(v, Value):
            self.v = v.v
            return
        if not Value.valid(v):
            raise ValueError("Invalid value")
        if is_instance(v, str):
            self.v = v.upper()
        else:
            self.v = v

    def __add__(self, other):
        if not all((self.isnum(), other.isnum())):
            raise TypeError("Can't add non-numbers")
        try:
            return Value(self.v + other.v)
        except ValueError:
            raise OverflowError("Number out of range")

    def __iadd__(self, other):
        self.v = (self + other).v

    def __sub__(self, other):
        if not all((self.isnum(), other.isnum())) and not all((self.isletter(), other.isletter())):
            raise TypeError("Can't subtract between different types")
        if self.isletter():
            return Value(ord(self.v) - ord(other.v))
        try:
            return Value(self.v - other.v)
        except ValueError:
            raise OverflowError("Number out of range")

    def __isub__(self, other):
        self.v = (self - other).v

    def inc(self):
        if not self.isnum():
            raise TypeError("Can only bump number")
        self += Value(1)

    def dec(self):
        if not self.isnum():
            raise TypeError("Can only bump number")
        self -= Value(1)

    def isnum(self):
        return is_instance(self.v, int)

    def isletter(self):
        return is_instance(self.v, str) and Value.valid(self)

    @staticmethod
    def valid(v):
        if is_instance(v, Value):
            return Value.valid(v.v)
        if is_instance(v, str):
            return len(v) == 1 and v.isalpha()
        if is_instance(v, int):
            return MIN_INT <= v <= MAX_INT
        return v is None

class Reference(object):
    def __init__(self, v):
        if is_instance(v, Value):
            v = v.v
        if not is_instance(v, int):
            raise TypeError("Index must be integer")
        if not 0 <= v <= data.MAX_INT:
            raise ValueError("Index out of range")
        self.v = v

    def __get__(self, obj, objtype=None):
        return obj[self.v]