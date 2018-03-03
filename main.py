#!/usr/bin/python3

from vm import VM
from parsing import readProgram, parseInput, parseOutput
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError("You need to specify a program")

    progName = sys.argv[1]
    with open(progName, 'r') as f:
        prog = readProgram(f)
    progIn = input()

    vm = VM(istream=parseInput(progIn), dynamicMem=prog.dynamicMem, initMem=prog.initMem)
    vm.cmd = prog.cmds
    vm.run()

    print(parseOutput(vm.ostream))
