import itertools
import math
import re
from enum import Enum
from typing import List, Set, Optional, Dict

from common import read_data


class Side(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @property
    def opposite(self):
        return Side((self.value + 2) % 4)


class Tile:
    def __init__(self, tile_map: Dict[complex, str]):
        self.tile_map = tile_map
        self.operations = "0"
        self.size_x = int(round(max(p.real for p in tile_map))) + 1
        self.size_y = int(round(max(p.imag for p in tile_map))) + 1
        self.size = self.size_x

    def row(self, row_id: int) -> str:
        return "".join(self.tile_map[complex(row_id, y)] for y in range(self.size))

    def column(self, col_id: int) -> str:
        return "".join(self.tile_map[complex(x, col_id)] for x in range(self.size))

    def identity(self) -> 'Tile':
        return self

    def rotate(self) -> 'Tile':
        i = complex(0, 1)
        m = complex(self.size_y - 1, 0)
        self.tile_map = {position * i + m: value for position, value in self.tile_map.items()}
        self.size_x, self.size_y = self.size_y, self.size_x
        self.operations += "R"
        if self.operations[-4:] == "RRRR":  # Identity
            self.operations = self.operations[:-4]
        return self

    def flip(self) -> 'Tile':
        self.tile_map = {complex(position.real, self.size_y - 1 - position.imag): value for position, value in
                         self.tile_map.items()}
        self.operations += "F"
        if self.operations[-2:] == "FF":  # Identity
            self.operations = self.operations[:-2]
        return self

    def apply_transformation(self):
        transformations = [lambda t: t.identity()] + [lambda t: t.rotate(), lambda t: t.flip(), lambda t: t.flip()] * 4
        for transformation in transformations:
            transformation(self)
            yield


class MapTile(Tile):
    def __init__(self, raw_tiles: str):
        lines = raw_tiles.split("\n")
        tile_map = {complex(x, y): char for y, line in enumerate(lines[1:]) for x, char in enumerate(line)}
        super().__init__(tile_map)
        self.tile_id = int(re.match(r".*(\d{4}).*", lines[0]).group(1))
        self._neighbour_ids: Set[int] = set()
        self.neighbours: List['MapTile'] = []

    def __repr__(self):
        return f"Tile {self.tile_id}{self._neighbour_ids} / {self.operations}"

    def map_border(self, side: Side) -> str:
        if side == Side.NORTH:
            return self.column(0)
        if side == Side.SOUTH:
            return self.column(self.size - 1)
        if side == Side.EAST:
            return self.row(self.size - 1)
        if side == Side.WEST:
            return self.row(0)

    def add_neighbour(self, other: 'MapTile') -> None:
        if other == self:
            return
        self._neighbour_ids.add(other.tile_id)
        self.neighbours.append(other)

    def side_neighbour(self, side: Side) -> Optional['MapTile']:
        own_border = self.map_border(side)
        mirror_border = own_border[::-1]
        for neighbour in self.neighbours:
            for other_side in Side:
                neighbour_border = neighbour.map_border(other_side)
                if neighbour_border == own_border or neighbour_border == mirror_border:
                    return neighbour
        return None

    def as_image(self) -> Dict[complex, str]:
        return {pos - complex(1, 1): value
                for pos, value in self.tile_map.items()
                if pos.real not in (0, self.size - 1) and pos.imag not in (0, self.size - 1)}


class SnakeTile(Tile):
    def __init__(self, map_lines: List[str]):
        tile_map = {complex(x, y): char for y, line in enumerate(map_lines) for x, char in enumerate(line)}
        super().__init__(tile_map)
        self.size_y = len(map_lines)
        self.size_x = len(map_lines[0])

    def pattern_dots(self) -> Set[complex]:
        return {pos for pos, value in self.tile_map.items() if value == "#"}


class ImageTile(Tile):
    def __init__(self, image_map: Dict[complex, str]):
        super().__init__(image_map)
        self.operations = ""

    def marked_dots(self) -> Set[complex]:
        return {pos for pos, value in self.tile_map.items() if value == "#"}


class JigsawMap:
    def __init__(self, raw_tiles):
        self.all_tiles = [MapTile(raw_tile) for raw_tile in raw_tiles]

        # Connect adjacent tiles together
        common_borders = {}
        for tile in self.all_tiles:
            for side in Side:
                border = tile.map_border(side)
                if border not in common_borders:
                    border = border[::-1]
                if border not in common_borders:
                    common_borders[border] = [tile]
                else:
                    common_borders[border].append(tile)

        for border in common_borders:
            for tile1, tile2 in itertools.combinations(common_borders[border], 2):
                tile1.add_neighbour(tile2)
                tile2.add_neighbour(tile1)

    @property
    def corner_tiles(self):
        return [t for t in self.all_tiles if len(t.neighbours) == 2]

    def as_image(self) -> Dict[complex, str]:

        def reposition_first_tile(tile):
            """ We want the first tile to be in the top left corner """
            for _ in tile.apply_transformation():
                if tile.side_neighbour(Side.EAST) and tile.side_neighbour(Side.SOUTH):
                    break

        def copy_tile_to_image(tile, image, tile_offset_x, tile_offset_y):
            for position, value in tile.as_image().items():
                position_in_map = position + complex(tile_offset_x, tile_offset_y)
                image[position_in_map] = value

        def get_next_tile(current, direction):
            tile = current.side_neighbour(direction)
            return (tile, False) if tile else (current.side_neighbour(Side.SOUTH), True)

        def align_tile_to_previous(tile_to_align, previous, direction):
            border = previous.map_border(direction)
            for _ in tile_to_align.apply_transformation():
                if tile_to_align.map_border(direction.opposite) == border:
                    return
            else:
                assert False, "Could not reposition!"

        current_tile = next(t for t in self.corner_tiles)
        tile_size = int(math.sqrt(len(current_tile.as_image())))
        merged_image = {}
        reposition_first_tile(current_tile)
        direction_x = Side.EAST
        current_row, current_column = 0, 0
        while True:
            copy_tile_to_image(current_tile, merged_image, current_column * tile_size, current_row * tile_size)
            next_tile, new_row = get_next_tile(current_tile, direction_x)
            if not next_tile:
                break
            align_tile_to_previous(next_tile, current_tile, Side.SOUTH if new_row else direction_x)
            # Move to next tile
            direction_x = direction_x.opposite if new_row else direction_x
            current_row += 1 if new_row else 0
            current_column += (1 if direction_x == Side.EAST else -1) if not new_row else 0
            current_tile = next_tile

        return merged_image


def part_1(print_result: bool = True) -> int:
    tiles = JigsawMap(read_data("20", False).split("\n\n"))

    checksum = math.prod(t.tile_id for t in tiles.corner_tiles)
    if print_result:
        print(f"Map checksum (corners) is {checksum}")
    return checksum


def part_2(print_result: bool = True) -> int:
    tiles = JigsawMap(read_data("20", False).split("\n\n"))

    image = ImageTile(tiles.as_image())
    sea_snake = SnakeTile(read_data("20b", True))
    sea_snake_dots = sea_snake.pattern_dots()

    snakes_found = 0
    for _ in image.apply_transformation():  # try in various modes
        image_dots = image.marked_dots()
        for y in range(image.size - sea_snake.size_y):
            for x in range(image.size - sea_snake.size_x):
                t = complex(x, y)
                translated_snake = {p + t for p in sea_snake_dots}
                if all(p in image_dots for p in translated_snake):
                    snakes_found += 1
        if snakes_found:
            break

    occupied = snakes_found * len(sea_snake_dots)
    habitat_roughness = len(image.marked_dots()) - occupied

    if print_result:
        print(f"Found {snakes_found} sea snakes on the image , for a water roughness factor of {habitat_roughness}")

    return habitat_roughness


SOLUTION_1 = 32287787075651
SOLUTION_2 = 1939

if __name__ == "__main__":
    part_1()
    part_2()
