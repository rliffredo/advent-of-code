from math import prod
from typing import Tuple, Iterator

from common import read_data


def parse_data():
    raw_map = read_data("03", True)
    tree_map = {(x, y) for y, line in enumerate(raw_map) for x, char in enumerate(line) if char == "#"}
    return tree_map, len(raw_map[0]), len(raw_map)


def make_slope(slope_params: Tuple[int, int], map_size: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    x, y = 0, 0
    while True:
        if y > map_size[1]:
            return
        yield x, y
        x = (x + slope_params[0]) % map_size[0]
        y = y + slope_params[1]


def get_hits_in_slope(map_info, x, y):
    tree_map, size_x, size_y = map_info
    slope = make_slope((x, y), (size_x, size_y))
    return sum(1 for position in slope if position in tree_map)


def part_1(print_result: bool = True) -> int:
    map_info = parse_data()
    hit_tree = get_hits_in_slope(map_info, 3, 1)
    if print_result:
        print(f"Trees hit: {hit_tree}")
    return hit_tree


def part_2(print_result: bool = True) -> int:
    map_info = parse_data()
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    hit_tree = prod(get_hits_in_slope(map_info, *slope) for slope in slopes)
    if print_result:
        print(f"Trees hit: {hit_tree}")
    return hit_tree


SOLUTION_1 = 162
SOLUTION_2 = 3064612320

if __name__ == "__main__":
    part_1()
    part_2()
