import itertools
import re
from dataclasses import dataclass
from typing import Tuple, List, Literal

from common import read_data


@dataclass
class Cuboid:
    state: Literal['on', 'off']
    x: Tuple[int, int]
    y: Tuple[int, int]
    z: Tuple[int, int]

    @staticmethod
    def from_raw_data(data) -> 'Cuboid':
        coords = [int(d) for d in data[1:]]
        return Cuboid(data[0], (coords[0], coords[1]), (coords[2], coords[3]), (coords[4], coords[5]), [])

    covered_by: List['Cuboid']

    @property
    def size(self):
        base = (self.x[1] - self.x[0] + 1) * (self.y[1] - self.y[0] + 1) * (self.z[1] - self.z[0] + 1)
        all_covered = sum(c.size for c in self.covered_by)
        return base - all_covered

    def intersect(self, other: 'Cuboid'):
        return Cuboid(
            self.state,
            (max(self.x[0], other.x[0]), min(self.x[1], other.x[1])),
            (max(self.y[0], other.y[0]), min(self.y[1], other.y[1])),
            (max(self.z[0], other.z[0]), min(self.z[1], other.z[1])),
            []
        )

    def add_cover(self, other: 'Cuboid'):
        if not self.overlaps(other):
            return
        overlap = other.intersect(self)
        for already_covering in self.covered_by:
            already_covering.add_cover(overlap)
        self.covered_by.append(overlap)

    def overlaps(self, other: 'Cuboid') -> bool:
        return (
                (other.x[0] <= self.x[1] and other.x[1] >= self.x[0]) and
                (other.y[0] <= self.y[1] and other.y[1] >= self.y[0]) and
                (other.z[0] <= self.z[1] and other.z[1] >= self.z[0])
        )


def parse_data() -> List[Cuboid]:
    def parse_line(line):
        m = re.match(r"([onf]+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line)
        return Cuboid.from_raw_data(m.groups())

    lines = read_data("22", True)
    commands = [parse_line(l) for l in lines if l]
    return commands


def get_active_cubes(cuboid_commands):
    # Step 1: build list of overlapping cuboids
    for cuboid_index, cuboid in enumerate(cuboid_commands):
        for other_cuboid in cuboid_commands[cuboid_index + 1:]:
            cuboid.add_cover(other_cuboid)
    # Step 2: just sum the sizes!
    active_cubes = sum(cuboid.size for cuboid in cuboid_commands if cuboid.state == "on")
    return active_cubes


def part_1(print_result: bool = True) -> int:
    cuboid_commands = parse_data()
    cuboid_commands = [c for c in cuboid_commands
                       if all(-50 < d < 50 for d in itertools.chain(c.x, c.y, c.z))]
    return get_active_cubes(cuboid_commands)


def part_2(print_result: bool = True) -> int:
    cuboid_commands = parse_data()
    return get_active_cubes(cuboid_commands)


SOLUTION_1 = 642125
SOLUTION_2 = 1235164413198198

if __name__ == "__main__":
    print(part_1())
    print(part_2())
