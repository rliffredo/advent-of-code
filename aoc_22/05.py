import re
from typing import List, Tuple

from more_itertools import split_at

from common import read_data


def parse_commands(commands_str: List[str]) -> List[Tuple[int, int, int]]:
    def parse_cmd(cmd):
        amt_, from_, to_ = map(int, re.match(r'move (\d+) from (\d+) to (\d+)', cmd).groups())
        return amt_, from_, to_

    return [parse_cmd(cmd) for cmd in commands_str]


def parse_stacks(stacks_str: List[str]):
    # fetch stack names and positions from last line
    stack_positions = [stacks_str[-1].find(str(n)) for n in range(10) if str(n) in stacks_str[-1]]
    # build now each stack
    stacks = [[] for n in range(len(stack_positions))]
    for stack_line in stacks_str[:-1][
                      ::-1]:  # I thought [:-1:-1] would have done it, but I could not get it working...
        for stack_id, stack_position in enumerate(stack_positions):
            if stack_position < len(stack_line) and stack_line[stack_position] != ' ':
                stacks[stack_id].append(stack_line[stack_position])
    return stacks


def parse_data():
    lines = [line for line in read_data("05", True)]
    stacks_str, commands_str = split_at(lines, lambda l: not l)
    return parse_stacks(stacks_str), parse_commands(commands_str)


def move_crates(crane, stacks, commands):
    for cmd in commands:
        crane(cmd, stacks)
    result = ''.join(map(list.pop, stacks))
    return result


def move_9000(cmd, stacks):
    for _ in range(cmd[0]):
        stacks[cmd[2] - 1].append(stacks[cmd[1] - 1].pop())


def part_1(print_result: bool = True) -> str:
    stacks, commands = parse_data()
    return move_crates(move_9000, stacks, commands)


def move_9001(cmd, stacks):
    from_stack = stacks[cmd[1] - 1]
    stacks[cmd[1] - 1], moved_cranes = from_stack[:-cmd[0]], from_stack[-cmd[0]:]
    stacks[cmd[2] - 1].extend(moved_cranes)


def part_2(print_result: bool = True) -> str:
    stacks, commands = parse_data()
    return move_crates(move_9001, stacks, commands)


SOLUTION_1 = 'JDTMRWCQJ'
SOLUTION_2 = 'VHJDDCWRD'

if __name__ == "__main__":
    print(part_1())
    print(part_2())
