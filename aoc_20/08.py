from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Callable

from common import read_data


@dataclass(eq=True, frozen=True)
class Registers:
    ip: int
    ac: int


class Opcode(str, Enum):
    NOP = "nop"
    ACC = "acc"
    JMP = "jmp"


@dataclass
class Instruction:
    opcode: Opcode
    params: List[int]


class GameConsole:
    # Instructions
    INSTRUCTION_SET = {
        Opcode.NOP: lambda registers, params: Registers(ip=registers.ip + 1, ac=registers.ac),
        Opcode.JMP: lambda registers, params: Registers(ip=registers.ip + params[0], ac=registers.ac),
        Opcode.ACC: lambda registers, params: Registers(ip=registers.ip + 1, ac=registers.ac + params[0]),
    }

    def __init__(self):
        self.registers = Registers(0, 0)
        self.instructions: List[Tuple[Callable, int]] = []

    def load(self, program: List[Instruction]):
        self.registers = Registers(0, 0)
        self.instructions = [(self.INSTRUCTION_SET[instruction .opcode], instruction.params) for instruction in program]

    def execute_step(self):
        instruction = self.instructions[self.registers.ip]
        self.registers = instruction[0](self.registers, instruction[1])

    def has_terminated(self):
        return self.registers.ip >= len(self.instructions)

    @staticmethod
    def parse_program(source_program: List[str]) -> List[Instruction]:
        def parse_instruction(line: str) -> Instruction:
            instruction_type, param = line.split()
            return Instruction(opcode=instruction_type, params=[int(param)])

        return [parse_instruction(line) for line in source_program]


def execute_until_loop(game_boy: GameConsole) -> Tuple[bool, List[Registers]]:
    states = set()
    states_sequence = []
    while game_boy.registers.ip not in states:
        if game_boy.has_terminated():
            return False, states_sequence
        states.add(game_boy.registers.ip)
        states_sequence.append(game_boy.registers)
        game_boy.execute_step()
    return True, states_sequence


def part_1():
    program = GameConsole.parse_program(read_data("08", True))
    game_boy = GameConsole()
    game_boy.load(program)
    _, states_sequence = execute_until_loop(game_boy)
    print(f"Last state before double execution: {states_sequence[-1]}")  # (528, 1331)


def part_2():
    def flip_instruction(instruction: Instruction) -> Instruction:
        flipped_opcode = {Opcode.JMP: Opcode.NOP, Opcode.NOP: Opcode.JMP, Opcode.ACC: Opcode.ACC}[instruction.opcode]
        return Instruction(opcode=flipped_opcode, params=instruction.params)

    program = GameConsole.parse_program(read_data("08", True))
    game_boy = GameConsole()
    game_boy.load(program)
    _, states_sequence = execute_until_loop(game_boy)
    affected_instructions = [state.ip for state in states_sequence]
    for ip in affected_instructions:
        fixed_program = [flip_instruction(instruction) if n == ip else instruction
                         for n, instruction in enumerate(program)]
        game_boy.load(fixed_program)
        is_looping, fixed_state_sequence = execute_until_loop(game_boy)
        if not is_looping:
            print(f"Last state before exit: {fixed_state_sequence[-1]}")  # (622, 1121)
            break
    else:
        assert False, "There _is_ a solution!"


part_1()
part_2()
