from data import Command, Value, Reference

class Program(object):
    def __init__(self):
        self.initMem = []
        self.cmds = []

def try_convert(s):
    try:
        return int(s)
    except ValueError:
        if s.lower() == 'none':
            return None
        return str(s)

def readProgram(stream):
    prog = Program()
    lines = [i.strip() for i in stream]
    if lines[0].split()[0] == 'mem':
        prog.initMem = [try_convert(i.strip()) for i in lines[0].split()[1:]]
        lines = lines[1:]

    for line in lines:
        cmd = [i.strip() for i in line.split()]
        prog.cmds += cmd
