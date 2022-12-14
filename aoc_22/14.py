from itertools import pairwise, chain

from common import read_data, print_map


def parse_data():
    def generate_rocks(rock1, rock2):
        rock1 = list(map(int, rock1.split(',')))
        rock2 = list(map(int, rock2.split(',')))
        return [
            (x, y)
            for y in range(min(rock1[1], rock2[1]), max(rock1[1], rock2[1]) + 1)
            for x in range(min(rock1[0], rock2[0]), max(rock1[0], rock2[0]) + 1)
        ]

    rock_lines = [line.split(' -> ') for line in read_data('14', True)]
    return set(chain.from_iterable(
        generate_rocks(start, end)
        for line in rock_lines
        for start, end in pairwise(line)
    ))


def calc_map_size(rocks):
    map_sizes = (
        min(r[0] for r in rocks),
        max(r[0] for r in rocks),
        0,
        max(r[1] for r in rocks),
    )
    return map_sizes


def map_to_color(x, y, rocks, sand):
    if (x, y) in rocks:
        return '#'
    if (x, y) in sand:
        return 'o'
    if (x, y) == (500, 0):
        return '+'
    return '.'


def move_sand_grain(current_sand, rocks, sands) -> tuple[int, int]:
    next_place = current_sand[0], current_sand[1] + 1
    if next_place not in rocks and next_place not in sands:
        return next_place
    next_place = current_sand[0] - 1, current_sand[1] + 1
    if next_place not in rocks and next_place not in sands:
        return next_place
    next_place = current_sand[0] + 1, current_sand[1] + 1
    if next_place not in rocks and next_place not in sands:
        return next_place
    return current_sand


def accumulate_sand(rocks, sands, stop_flow_condition):
    current_sand = 500, 0
    while True:
        new_sand = move_sand_grain(current_sand, rocks, sands)
        if stop_flow_condition(new_sand):
            break
        if new_sand == current_sand:
            sands.add(current_sand)
            current_sand = 500, 0
        else:
            current_sand = new_sand


def part_1(print_results: bool = False) -> int:
    rocks = parse_data()
    map_sizes = calc_map_size(rocks)
    sands = set()
    accumulate_sand(rocks, sands, lambda sand: not map_sizes[0] <= sand[0] <= map_sizes[1])
    if print_results:
        print_map(map_sizes, lambda x, y: map_to_color(x, y, rocks, sands))
    return len(sands)


def part_2() -> int:
    rocks = parse_data()
    map_sizes = calc_map_size(rocks)
    height = map_sizes[3] - map_sizes[2] + 2
    rocks |= {(x, map_sizes[3]+2) for x in range(map_sizes[0] - height, map_sizes[1] + height)}
    sands = set()
    accumulate_sand(rocks, sands, lambda sand: sand == (500, 0))
    return len(sands) + 1


SOLUTION_1 = 672
SOLUTION_2 = 26831

if __name__ == '__main__':
    print(part_1(True))
    print(part_2())
