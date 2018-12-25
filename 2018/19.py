from array import array
from dataclasses import dataclass


@dataclass
class Instruction:
    opcode: str
    a: int
    b: int
    c: int


class ProgramOverflowError(Exception):

    def __init__(self, memory, ip, program, last_instruction, cycle_count):
        self.memory = memory
        self.ip = ip
        self.program = program
        self.last_instruction = last_instruction
        self.cycles = cycle_count

    def __str__(self):
        return f'Overflow error after {self.cycles} cycles. IP: {self.ip}, memory: {self.memory}'


class Cpu:
    opcodes = {
        'addr': lambda a, b, m: m[a] + m[b],
        'addi': lambda a, b, m: m[a] + b,
        'mulr': lambda a, b, m: m[a] * m[b],
        'muli': lambda a, b, m: m[a] * b,
        'banr': lambda a, b, m: m[a] & m[b],
        'bani': lambda a, b, m: m[a] & b,
        'borr': lambda a, b, m: m[a] | m[b],
        'bori': lambda a, b, m: m[a] | b,
        'setr': lambda a, b, m: m[a],
        'seti': lambda a, b, m: a,
        'gtir': lambda a, b, m: 1 if a > m[b] else 0,
        'gtri': lambda a, b, m: 1 if m[a] > b else 0,
        'gtrr': lambda a, b, m: 1 if m[a] > m[b] else 0,
        'eqir': lambda a, b, m: 1 if a == m[b] else 0,
        'eqri': lambda a, b, m: 1 if m[a] == b else 0,
        'eqrr': lambda a, b, m: 1 if m[a] == m[b] else 0,
    }

    def __init__(self, ip_register, memory, inspect=False):
        self.ip_register = ip_register
        self.ip = 0
        self.memory = memory
        self.program = None
        self.cycles = 0
        self.inspect = inspect

    def load_program(self, program):
        self.program = program

    def dump_state(self):
        if not self.inspect:
            return
        print(f'R0: {self.memory[0]:5} '
              f'R1: {self.memory[1]:5} '
              f'R2: {self.memory[2]:5} '
              f'R3: {self.memory[3]:5} '
              f'R4: {self.memory[4]:5} '
              f'R5: {self.memory[5]:5}')

    def exec(self):
        max_instruction = len(self.program)
        while True:
            self.cycles += 1
            instruction = self.exec_cycle()
            self.dump_state()
            if not 0 <= self.ip < max_instruction:
                raise ProgramOverflowError(self.memory, self.ip, self.program, instruction, self.cycles)

    def exec_cycle(self):
        self.memory[self.ip_register] = self.ip
        instruction = self.program[self.ip]
        operation = self.opcodes[instruction.opcode]
        self.memory[instruction.c] = operation(instruction.a, instruction.b, self.memory)
        self.ip = self.memory[self.ip_register] + 1
        return instruction


def read_program():
    file_data = open('input_19.txt').readlines()
    file_data = [line.strip('\n') for line in file_data]
    return file_data


def parse_program(raw_data):
    register_line = raw_data[0]
    assert register_line[0] == '#'
    ip_register = int(register_line.split()[1])
    program_lines = [line.split() for line in raw_data[1:] if line]
    return ip_register, [Instruction(l[0], int(l[1]), int(l[2]), int(l[3])) for l in program_lines]


data = read_program()
parsed_ip_register, parsed_program = parse_program(data)
cpu = Cpu(parsed_ip_register, array('l', [0, 0, 0, 0, 0, 0]), False)
cpu.load_program(parsed_program)
try:
    cpu.exec()
except ProgramOverflowError as e:
    print(e)


# -> 1920, 946, 946, 1, 256, 945


# Translation and comments on the input
#
# ip = 16       # GOTO 17  (this line is reached only once!)
# m[1] = 1
# m[2] = 1
# m[3] = m[1] * m[2]
# m[3] = m[3] == m[5]  # if ... together with below
# ip = ip + m[3]       # if (above) GOTO 7 else GOTO 6
# ip = ip + 1          # GOTO 8
# m[0] = m[0] + m[1]
# m[2] = m[2] + 1
# m[3] = m[2] > m[5]   # if .... with below
# ip = ip + m[3]       # exit loop
# ip = 2               # GOTO 3
# m[1] = m[1] + 1
# m[3] = m[1] > m[5]   # if ... with below
# ip = ip + m[3]       # exit loop
# ip = 1               # GOTO 2
# ip = ip * ip         # halt condition?
# m[5] = 2             # line 17... here we are building 5
# m[5] = m[5] * m[5]
# m[5] = m[5] * ip
# m[5] = m[5] * 11
# m[3] = m[3] + 4
# m[3] = m[3] * ip
# m[3] = m[3] + 21
# m[5] = m[5] + m[3]
# ip = ip + m[0]       # m[0] zero for the easy -- otherwise do full initialization
# ip = m[0] + 5        # GOTO 6 -> we can play (easy)
# m[3] = ip
# m[3] = m[3] * ip
# m[3] = m[3] + ip
# m[3] = m[3] * ip
# m[3] = m[3] + 14
# m[3] = m[3] + ip
# m[5] = m[3] + m[5]
# m[0] = m[0] + 2
# ip = 0              # GOTO 1 -> play hard

##########


def first_translation():
    ret = 0
    target = 10551345
    m1 = 1
    while m1 <= target:
        m2 = 1
        while m2 <= target:
            if (m1 * m2) == target:
                ret += m1
            m2 += 1
        m1 += 1
    return ret


def refactored_fast():
    ret = 0
    target = 10551345
    for i in range(target):
        m1 = i + 1
        if target % m1 == 0:
            ret += m1
    return ret


print(refactored_fast())

# -> 19354944
