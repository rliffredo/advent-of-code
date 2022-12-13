import itertools
from collections import defaultdict

from advent_of_code_ocr import convert_6

from common import read_data


def parse_data():
    def parse_command(command: str):
        match command.split():
            case ['noop']:
                return [lambda _: _]
            case ['addx', amt]:
                return [lambda _: _, lambda x: x + int(amt)]

    commands = [parse_command(line) for line in read_data('10', True) if line]
    return list(itertools.chain.from_iterable(commands))


def execute(clock_instructions, x_side_effect):
    x = 1
    for n, current_cmd in enumerate(clock_instructions):
        x_side_effect(n, x)
        x = current_cmd(x)


def part_1(print_result: bool = True) -> int:
    clock_instructions = parse_data()
    signal_strengths = []
    execute(clock_instructions, lambda n, x: signal_strengths.append(x * (n + 1)))
    interesting = [signal_strengths[n - 1] for n in (20, 60, 100, 140, 180, 220)]
    return sum(interesting)


def part_2(print_result: bool = True) -> str:
    clock_instructions = parse_data()
    pixels = defaultdict(list)
    execute(clock_instructions, lambda n, x: pixels[(n // 40)].append('#' if x - 1 <= (n % 40) <= x + 1 else '.'))
    # display uses six lines
    display = '\n'.join([''.join(pixels[line]) for line in range(6)])
    return convert_6(display)


SOLUTION_1 = 14360
SOLUTION_2 = 'BGKAEREZ'

if __name__ == '__main__':
    print(part_1())
    print(part_2())
