import itertools
from collections import defaultdict, Counter
from enum import Enum
from functools import lru_cache
from typing import List, Tuple

from common import read_data


class Direction(str, Enum):
    east = "e"
    southeast = "se"
    southwest = "sw"
    west = "w"
    northwest = "nw"
    northeast = "ne"

    @property
    def offset(self) -> Tuple[int, int, int]:
        """ x, y, z """
        return {
            Direction.east: (1, -1, 0),
            Direction.southeast: (0, -1, 1),
            Direction.southwest: (-1, 0, 1),
            Direction.west: (-1, 1, 0),
            Direction.northwest: (0, 1, -1),
            Direction.northeast: (1, 0, -1),
        }[self]


ALL_OFFSET = [Direction(m).offset for m in Direction]


def parse_tile_path(raw_path: str) -> List[Direction]:
    path = []
    buffer = ""
    allowed_values = [d for d in Direction]
    for char in raw_path:
        buffer += char
        if buffer in allowed_values:
            path.append(Direction(buffer))
            buffer = ""
    return path


def sum_position(p1, p2):
    p1x, p1y, p1z = p1
    p2x, p2y, p2z = p2
    return p1x + p2x, p1y + p2y, p1z + p2z


def identify_black_tiles(tiles_paths):
    all_tiles = defaultdict(bool)
    for tile_id, path_to_tile in enumerate(tiles_paths):
        current_pos = (0, 0, 0)
        for movement in path_to_tile:
            current_pos = sum_position(current_pos, movement.offset)
        all_tiles[current_pos] = not all_tiles[current_pos]
    return {tile_position for tile_position, tile_is_black in all_tiles.items() if tile_is_black}


def part_1(print_result: bool = True) -> int:
    raw_data = read_data("24", True)
    tiles_paths = [parse_tile_path(line) for line in raw_data]

    all_black_tiles = identify_black_tiles(tiles_paths)
    result = len(all_black_tiles)

    if print_result:
        print(f"Number of black tiles: {result}")
    return result


@lru_cache(maxsize=15_000)
def neighbour_positions(tile_position):
    return tuple(sum_position(tile_position, offset) for offset in ALL_OFFSET)


def flip_tiles(all_black_tiles):
    blacks_with_white_neighbours = {t: [n for n in neighbour_positions(t) if n not in all_black_tiles]
                                    for t in all_black_tiles}
    white_with_count_black_neighbours = Counter(itertools.chain.from_iterable(blacks_with_white_neighbours.values()))

    still_blacks = {black for black, whites in blacks_with_white_neighbours.items() if len(whites) in (4, 5)}
    new_blacks = {white for white, blacks in white_with_count_black_neighbours.items() if blacks == 2}

    return still_blacks | new_blacks


def part_2(print_result: bool = True) -> int:
    raw_data = read_data("24", True)
    tiles_paths = [parse_tile_path(line) for line in raw_data]

    all_black_tiles = identify_black_tiles(tiles_paths)
    for day in range(100):
        all_black_tiles = flip_tiles(all_black_tiles)
    result = len(all_black_tiles)

    if print_result:
        print(f"Number of black tiles after 100 days: {result}")
    return result


SOLUTION_1 = 373
SOLUTION_2 = 3917

if __name__ == "__main__":
    part_1()
    part_2()
