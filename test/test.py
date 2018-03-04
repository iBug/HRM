#!/usr/bin/python3

import sys
import subprocess as sub

EXE = None

def runTest(progName, progIn, progOut):
    runCmd = ['python3', EXE, progName]
    prog = sub.run(runCmd, input=progIn.encode('ascii'), stdout=sub.PIPE)
    assert prog.returncode == 0
    #print(prog.stdout.decode('ascii').strip() + '\n' + progOut.strip())
    assert prog.stdout.decode('ascii').strip() == progOut.strip()

if __name__ == '__main__':
    assert len(sys.argv) >= 2
    EXE = sys.argv[1]

    runTest('test.hrm',
            '18 97 36 45 0 V U A R X M P 0 9 4 7 5 8 1 0 U Z Q B L E F X 0',
            '18 36 45 97 A M P R U V X 1 4 5 7 8 9 B E F L Q U X Z')
