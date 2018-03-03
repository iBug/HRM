from data import Command, CommandError, Value, Reference

COMMANDS = {}
JUMPS = {}

def command(*junk, aliases=None, incr_pc=True, is_jump=False):
    def decorator(func):
        global COMMANDS, JUMPS

        def f(vm, *args):
            ret = func(vm, *args)
            if incr_pc:
                vm.core.pc += 1
            return ret

        COMMANDS[func.__name__] = f
        if aliases is not None:
            for a in aliases:
                COMMANDS[a] = f

        if is_jump:
            JUMPS[func.__name__] = True
            if aliases is not None:
                for i in aliases:
                    JUMPS[i] = True

        return f
    return decorator

@command(aliases=['in', 'input'])
def inbox(vm):
    try:
        vm.core.ax = vm.istream[0]
        vm.istream = vm.istream[1:]
        return True
    except IndexError:
        vm.core.ax = Value(None)
        raise CommandError("reached end of input")
    
@command(aliases=['out', 'output'])
def outbox(vm):
    if vm.core.ax == Value(None):
        raise CommandError('You have nothing to outbox')
    vm.ostream.append(vm.core.ax.copy())
    vm.core.ax = Value(None)
    return True

@command(incr_pc=False, is_jump=True)
def jump(vm, line):
    vm.core.pc = line
    return True

@command(aliases=['jumpz', 'jump_if_zero'], incr_pc=False, is_jump=True)
def jz(vm, line):
    if vm.core.ax == None:
        raise ValueError("You have nothing to test")
    if vm.core.ax.zero():
        vm.core.pc = line
    else:
        vm.core.pc += 1
    return True

@command(aliases=['jumpn', 'jump_if_negative'], incr_pc=False, is_jump=True)
def jn(vm, line):
    if not vm.core.ax.isnum():
        raise ValueError("You can only test a number")
    if vm.core.ax.neg():
        vm.core.pc = line
    else:
        vm.core.pc += 1
    return True

def getMemIndex(vm, v):
    if isinstance(v, Reference):
        return getMemIndex(vm, vm.getMem(v.v))
    if isinstance(v, Value):
        if v.isnum():
            return v.v
        raise TypeError("You can only use a number as index")
    return v

@command()
def copyto(vm, target):
    vm.setMem(getMemIndex(vm, target), vm.core.ax)
    return True

@command()
def copyfrom(vm, target):
    vm.core.ax = vm.getMem(getMemIndex(vm, target))
    return True

@command()
def add(vm, target):
    vm.core.ax += vm.getMem(getMemIndex(vm, target))
    return True

@command()
def sub(vm, target):
    vm.core.ax -= vm.getMem(getMemIndex(vm, target))
    return True

@command(aliases=['bump+'])
def bumpup(vm, target):
    # Don't call COPYFROM and COPYTO directly, they will increment the program counter
    vm.core.ax = vm.getMem(getMemIndex(vm, target))
    vm.core.ax += Value(1)
    vm.setMem(getMemIndex(vm, target), vm.core.ax)
    return True

@command(aliases=['bump-', 'bumpdn'])
def bumpdown(vm, target):
    vm.core.ax = vm.getMem(getMemIndex(vm, target))
    vm.core.ax -= Value(1)
    vm.setMem(getMemIndex(vm, target), vm.core.ax)
    return True

def getCommand(cmd):
    try:
        return COMMANDS[cmd]
    except KeyError:
        raise NameError('No such command "{}"'.format(cmd))

def runCommand(vm, cmd, *cmdArgs):
    vm.runCmd(Command(cmd, *cmdArgs))

def isJump(cmd):
    return cmd in JUMPS
