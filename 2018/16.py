import re
from collections import namedtuple
from dataclasses import dataclass


class Memory(namedtuple('Memory', 'r0,r1,r2,r3')):
    def with_register(self, index, value):
        assert 0 <= index < 4
        values = [value if index == pos else self[pos] for pos in (0, 1, 2, 3)]
        return Memory(*values)


@dataclass
class Instruction:
    opcode: int
    a: int
    b: int
    c: int


@dataclass
class Sampling:
    before: Memory
    instruction: Instruction
    after: Memory


def read_data():
    data = open('input_16a.txt').readlines()
    data = [line.strip('\n') for line in data]
    return data


def parse(data):
    samplings = []
    buffer = []
    for line in data:
        if not line.strip():
            continue
        buffer.append(line)
        if len(buffer) == 3:
            sampling = parse_sampling(buffer)
            samplings.append(sampling)
            buffer.clear()
    assert len(buffer) == 0
    return samplings


def parse_sampling(lines):
    try:
        m = re.match('Before:\s+\[(\d+), (\d+), (\d+), (\d+)\]', lines[0])
        before = Memory(*[int(n) for n in m.groups()])
        m = re.match('(\d+) (\d+) (\d+) (\d+)', lines[1])
        instruction = Instruction(*[int(n) for n in lines[1].split()])
        m = re.match('After:\s+\[(\d+), (\d+), (\d+), (\d+)\]', lines[2])
        after = Memory(*[int(n) for n in m.groups()])
        sample = Sampling(before=before, instruction=instruction, after=after)
        return sample
    except:
        print(lines)
        raise


opcodes = {
    'addr': lambda a, b, c, m: m.with_register(c, m[a]+m[b]),
    'addi': lambda a, b, c, m: m.with_register(c, m[a]+b),
    'mulr': lambda a, b, c, m: m.with_register(c, m[a]*m[b]),
    'muli': lambda a, b, c, m: m.with_register(c, m[a]*b),
    'banr': lambda a, b, c, m: m.with_register(c, m[a] & m[b]),
    'bani': lambda a, b, c, m: m.with_register(c, m[a] & b),
    'borr': lambda a, b, c, m: m.with_register(c, m[a] | m[b]),
    'bori': lambda a, b, c, m: m.with_register(c, m[a] | b),
    'setr': lambda a, b, c, m: m.with_register(c, m[a]),
    'seti': lambda a, b, c, m: m.with_register(c, a),
    'gtir': lambda a, b, c, m: m.with_register(c, 1 if a > m[b] else 0),
    'gtri': lambda a, b, c, m: m.with_register(c, 1 if m[a] > b else 0),
    'gtrr': lambda a, b, c, m: m.with_register(c, 1 if m[a] > m[b] else 0),
    'eqir': lambda a, b, c, m: m.with_register(c, 1 if a == m[b] else 0),
    'eqri': lambda a, b, c, m: m.with_register(c, 1 if m[a] == b else 0),
    'eqrr': lambda a, b, c, m: m.with_register(c, 1 if m[a] == m[b] else 0),
}


def matching_opcodes(sampling):
    return [
        opcode
        for opcode, operation in opcodes.items()
        if operation(sampling.instruction.a, sampling.instruction.b, sampling.instruction.c, sampling.before) == sampling.after
    ]

def more_than_three(samplings):
    equivalence = [matching_opcodes(sampling) for sampling in samplings]
    three_or_more = [eq for eq in equivalence if len(eq) >= 3]
    print(f'The number of instructions with three or more possible opcodes is {len(three_or_more)}')

data = read_data()
samplings = parse(data)
more_than_three(samplings)

#############

def get_opcode_mapping(samplings):
    equivalence = [(sampling.instruction.opcode, sorted(matching_opcodes(sampling)))
                   for sampling in samplings]
    eqs = {}
    mappings = {}
    for i in range(16):
        all_eqs = [eq for eq in equivalence if eq[0]==i]
        e = set(all_eqs[0][1])
        for eq in all_eqs:
            e.intersection_update(eq[1])
        eqs[i] = e
    while len(mappings) < 16:
        for code in eqs:
            if len(eqs[code])==1:
                mappings[code] = eqs[code].pop()
        for opcode in mappings.values():
            for opcodes in eqs.values():
                opcodes.difference_update({opcode})
    return mappings


def read_program():
    data = open('input_16b.txt').readlines()
    data = [line.strip('\n') for line in data]
    return data

def parse_program(program):
    return [Instruction(*[int(n) for n in line.split()]) for line in program]

def exec_instruction(instruction, memory, opcode_mapping):
    opcode = opcode_mapping[instruction.opcode]
    operation = opcodes[opcode]
    mem = operation(instruction.a, instruction.b, instruction.c, memory)
    # print(f'Executing {opcode} | A:{instruction.a} | B:{instruction.b} C:{instruction.c} on {memory} -> {mem}')
    return mem

def execute(program, opcode_mapping):
    memory = Memory(0, 0, 0, 0)
    for instruction in program:
        memory = exec_instruction(instruction, memory, opcode_mapping)
    return memory

def guess_and_execute(samplings):
    mapping = get_opcode_mapping(samplings)
    program_source = read_program()
    program = parse_program(program_source)
    final_memory = execute(program, mapping)
    print(f'The value of register R0 at the end of program is : {final_memory.r0}')

guess_and_execute(samplings)
