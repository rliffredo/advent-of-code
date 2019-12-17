from itertools import chain
from typing import Union

from common import read_data, intcode, get_map_dimensions, distance, pairwise


class AsciiBot:
    def __init__(self):
        self.computer = intcode.IntCode(lambda: 0, self.collect_scaffold)
        self.computer.load(read_data("17"))
        self.scaffold_output: Union[str, list] = []

    def run(self):
        self.computer.execute()
        self.scaffold_output = ''.join(self.scaffold_output)

    def collect_scaffold(self, value):
        self.scaffold_output.append(chr(value))


def map_from_scaffold(scaffold_printout):
    scaffold_map = {}
    lines = scaffold_printout.split('\n')
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            scaffold_map[(x, y)] = char
    return scaffold_map


def is_intersection(scaffold_map, x, y):
    return all(c == '#' for c in (
        scaffold_map[(x, y)],
        scaffold_map[(x - 1, y)],
        scaffold_map[(x + 1, y)],
        scaffold_map[(x, y - 1)],
        scaffold_map[(x, y + 1)],
    ))


def find_intersections(scaffold_map):
    intersections = []
    min_x, max_x, min_y, max_y = get_map_dimensions(scaffold_map)
    for x in range(min_x + 1, max_x):
        for y in range(min_y + 1, max_y):
            if is_intersection(scaffold_map, x, y):
                intersections.append((x, y))
    return sum(x * y for x, y in intersections)


bot = AsciiBot()
bot.run()
print(bot.scaffold_output)

scaffold = map_from_scaffold(bot.scaffold_output)
print(f'Map alignment code is {find_intersections(scaffold)}')  # 2660


################
# ## PART 2 ## #
################

def find_bot(scaffold_map):
    min_x, max_x, min_y, max_y = get_map_dimensions(scaffold_map)
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if scaffold_map[x, y] in ('^', 'v', '<', '>'):
                return (x, y), scaffold_map[x, y]
    else:
        assert False, 'Bot was on the map'


def move_forward(position, direction, scaffold_map):
    original_position = position
    while True:
        new_position = advance(direction, position)
        if new_position not in scaffold_map or scaffold_map[new_position] != '#':
            break
        position = new_position
    return distance(original_position, position), position


def advance(direction, position):
    new_position = (
        position[0] + (1 if direction == '>' else -1 if direction == '<' else 0),
        position[1] + (1 if direction == 'v' else -1 if direction == '^' else 0),
    )
    return new_position


def get_left(direction):
    return {'^': '<', 'v': '>', '<': 'v', '>': '^'}[direction]


def get_right(direction):
    return {'^': '>', 'v': '<', '<': '^', '>': 'v'}[direction]


def left_or_right(position, direction, scaffold_map):
    assert advance(direction, position) not in scaffold_map or scaffold_map[advance(direction, position)] != '#'
    left = advance(get_left(direction), position)
    if left in scaffold_map and scaffold_map[left] == '#':
        return 'L', get_left(direction)
    right = advance(get_right(direction), position)
    if right in scaffold_map and scaffold_map[right] == '#':
        return 'R', get_right(direction)
    return None, direction


def make_full_path(scaffold_map):
    position, direction = find_bot(scaffold_map)

    commands = []
    while True:
        forward, position = move_forward(position, direction, scaffold_map)
        if forward:
            commands.append(forward)
        turn, direction = left_or_right(position, direction, scaffold_map)
        if turn:
            commands.append(turn)
        else:
            break

    return commands


print('\nAnalyze path and manually create program')
path = make_full_path(scaffold)
path_pairs = [p for p in pairwise(path) if p[0] in ('L', 'R')]
print('Path for bot:')
for p in path_pairs:
    print(f' - {p[0]}{p[1]}')

A = (('L', 10), ('R', 8), ('L', 6), ('R', 6))
B = (('L', 8), ('L', 8), ('R', 8))
C = (('R', 8), ('L', 6), ('L', 10), ('L', 10))
path_comp = [A, B, A, C, A, B, C, B, C, B]

print(f'Program is equivalent to original path: {list(chain.from_iterable(path_comp)) == path_pairs}')


class RootedAsciiBot:
    PROGRAM = '\n'.join([
        'A,B,A,C,A,B,C,B,C,B',
        ','.join([f'{t}' for t in chain.from_iterable(A)]),
        ','.join([f'{t}' for t in chain.from_iterable(B)]),
        ','.join([f'{t}' for t in chain.from_iterable(C)]),
        'n',
    ]) + '\n'

    def __init__(self):
        self.computer = intcode.IntCode(self.provide_input, self.collect_output)
        self.computer.load(read_data("17"))
        self.computer.memory[0] = 2
        self.input_generator = (ord(i) for i in RootedAsciiBot.PROGRAM)
        self.collected_dust = 0

    def run(self):
        self.computer.execute()

    def collect_output(self, value):
        self.collected_dust = value

    def provide_input(self):
        return next(self.input_generator)


ascii_bot = RootedAsciiBot()
ascii_bot.run()
print(f'Collected dust: {ascii_bot.collected_dust}')  # 790595
