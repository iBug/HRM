from data import Command, Value, Reference
from command import isJump

class Program(object):
    def __init__(self):
        self.dynamicMem = False
        self.initMem = []
        self.cmds = []
        self.tags = {}

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
    while True:
        meta = lines[0].split()
        meta[0] = meta[0].lower()
        if meta[0] == 'mem':
            prog.initMem = [parseArg(i.strip()) for i in meta[1:]]
            lines = lines[1:]
            continue
        if meta[0] == 'memlen':
            memlen = int(meta[1])
            assert 0 < memlen <= MAX_INT
            prog.dynamicMem = False
            prog.initMem += [Value(None)] * (memlen - len(prog.initMem) if len(prog.initMem) <= memlen else 0 )
            continue
        break

    jumps = []  # Later we're going to parse the tags

    for line in lines:
        cmd = [i.strip() for i in line.split()]
        if cmd[0].startswith(':'):  # This is a jump tag!
            prog.tags[cmd[0][1:]] = len(prog.cmds)
            continue

        cmd[0] = cmd[0].lower()
        if isJump(cmd[0]):
            jumps.append(len(prog.cmds))  # Record jumps
            prog.cmds.append( Command(cmd[0], *cmd[1]) )
            continue
        prog.cmds.append( Command(cmd[0], *[parseArg(i) for i in cmd[1:]]) )

    for i in jumps:
        # Lookup and replace
        try:
            prog.cmds[i].ops[0] = prog.tags[prog.cmds[i].ops[0]]
        except KeyError:
            raise ValueError('No such tag "{}"'.format(prog.cmds[i].ops[0]))

    return prog

def parseInput(s):
    return [parseArg(i) for i in s.split()]

def parseOutput(outList):
    return ' '.join([str(i) for i in outList])
