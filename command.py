from data import Command, Value, Reference
from vm import VM

COMMANDS = {}

def command(aliases=None):
    global COMMANDS

    COMMANDS[func.__name__] = func
    if aliases is not None:
        for a in aliases:
            COMMANDS[a] = func

    def decorator(func):
        # Nothing to do here
        return func
    return decorator

@command(aliases=['in', 'input'])
def inbox(vm):
    try:
        vm.ax = vm.istream[0]
        return True
    except IndexError:
        vm.ax = Value(None)
        return False
    
@command(aliases=['out', 'output'])
def outbox(vm):
    vm.ostream += [vm.ax]
    return True

@command()
def jump(vm, line):
    vm.core.pc = line
    return True

@command(aliases=['jump_if_zero'])
def jz(vm, line):
    if vm.core.ax == None:
        raise ValueError("You have nothing to test")
    if vm.core.ax == 0:
        vm.core.pc = line
    return True

@command(aliases=['jump_if_negative'])
def jn(vm, line):
    if not vm.core.isnum():
        raise ValueError("You can only test a number")
    if vm.core.ax < 0:
        vm.core.pc = line
    return True

def getMemIndex(vm, v):
    if is_instance(v, Reference):
        return getMemIndex(vm.getMem(v.v))
    if is_instance(v, Value):
        if v.isnum():
            return v.v
        raise TypeError("You can only use a number as index")
    return v

@command()
def copyto(vm, target):
    vm.setMem(getMemIndex(target), vm.core.ax)
    return True

@command()
def copyfrom(vm, target):
    vm.core.ax = vm.getMem(getMemIndex(target))
    return True

@command()
def add(vm, target):
    vm.core.ax += vm.getMem(getMemIndex(target))
    return True

@command()
def sub(vm, target):
    vm.core.ax -= vm.getMem(getMemIndex(target))
    return True

@command(aliases=['bump+'])
def bumpup(vm, target):
    vm.runCmd(copyfrom, target)
    vm.core.ax += Value(1)
    vm.runCmd(copyto, target)
    return True

@command(aliases=['bump-', 'bumpdn'])
def bumpdown(vm, target):
    vm.runCmd(copyfrom, target)
    vm.core.ax -= Value(1)
    vm.runCmd(copyto, target)
    return True


def runCommand(cmd, vm, *cmdArgs)
    try:
        vm.runCmd(COMMAND[cmd], *cmdArgs)
    except IndexError:
        raise NameError("No such command")
