from data import Command, Value, Reference

class Program(object):
    def __init__(self):
        self.initMem = []
        self.cmds = []

def parseArg(s):
    if s.lower in ('none', '_'):
        return Value(None)
    if s.startswith('[') and s.endswith(']'):
        return Reference(int(s[1:-1]))
    try:
        return Value(int(s))
    except ValueError:
        if len(s) != 1:
            raise ValueError('"{}" is not an argument'.format(s))
        return Value(s)

def readProgram(stream):
    prog = Program()
    lines = [i.strip() for i in stream]
    if lines[0].split()[0] == 'mem':
        prog.initMem = [try_convert(i.strip()) for i in lines[0].split()[1:]]
        lines = lines[1:]

    for line in lines:
        cmd = [i.strip() for i in line.split()]
        cmd = Command(cmd[0], *[parseArg(i) for i in cmd[1:]])
        prog.cmds += cmd

def parseInput(s):
    return [parseArg(i) for i in s.split()]

def parseOutput(outList):
    return ' '.join([str(i.v) for i in outList])
