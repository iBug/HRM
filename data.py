MAX_INT = 999
MIN_INT = -999

class Command(object):
    def __init__(self, cmd, *ops):
        self.cmd = cmd  # Command
        self.ops = list(ops)  # Operands

    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return self.cmd + (' ' + ' '.join([str(i) for i in self.ops]) if len(self.ops) else '')

class CommandError(Command, Exception):
    pass

class Value(object):
    def __init__(self, v=None):
        if isinstance(v, Value):
            self.v = v.v
            return
        if not Value.valid(v):
            raise ValueError("Invalid value")
        if isinstance(v, str):
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
        return self

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
        return self

    def zero(self):
        return self.v == 0

    def neg(self):
        return self.isnum() and self.v < 0

    def inc(self):
        if not self.isnum():
            raise TypeError("Can only bump number")
        self += Value(1)

    def dec(self):
        if not self.isnum():
            raise TypeError("Can only bump number")
        self -= Value(1)

    def isnum(self):
        return isinstance(self.v, int)

    def isletter(self):
        return isinstance(self.v, str) and Value.valid(self)

    def __str__(self):
        return str(self.v)

    def __repr__(self):
        return str(self.v)

    def copy(self):
        return Value(self.v)

    @staticmethod
    def valid(v):
        if isinstance(v, Value):
            return Value.valid(v.v)
        if isinstance(v, str):
            return len(v) == 1 and v.isalpha()
        if isinstance(v, int):
            return MIN_INT <= v <= MAX_INT
        return v is None

class Reference(object):
    def __init__(self, v):
        if isinstance(v, Value):
            v = v.v
        if not isinstance(v, int):
            raise TypeError("Index must be integer")
        if not 0 <= v <= MAX_INT:
            raise ValueError("Index out of range")
        self.v = v

    def __get__(self, obj, objtype=None):
        return obj[self.v]

    def __str__(self):
        return '[{}]'.format(self.v)

    def __repr__(self):
        return '[{}]'.format(self.v)
