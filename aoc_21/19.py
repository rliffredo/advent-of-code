import itertools
from dataclasses import dataclass
from typing import Tuple, List, Set, Dict

from common import read_data


@dataclass(frozen=True)
class Point3D:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __lt__(self, other):
        return self.x, self.y, self.z < other.x, other.y, other.z

    def rotate(self, m):
        x = self.x * m[0][0] + self.y * m[0][1] + self.z * m[0][2]
        y = self.x * m[1][0] + self.y * m[1][1] + self.z * m[1][2]
        z = self.x * m[2][0] + self.y * m[2][1] + self.z * m[2][2]
        rp = Point3D(x, y, z)
        assert abs(self.x) + abs(self.y) + abs(self.z) == abs(rp.x) + abs(rp.y) + abs(rp.z), f"Matrix {m} is wrong?"
        return rp

    @property
    def distance(self):
        return self.x + self.y + self.z


Scanner = Tuple[int, List[Point3D]]


def parse_data() -> List[Scanner]:
    lines = read_data("19", True)
    scanners = []
    current_scanner = []
    for line in lines:
        if not line:
            continue
        if line.startswith("---"):
            if current_scanner:
                scanners.append((len(scanners), current_scanner))
            current_scanner = []
            continue
        p = line.split(",")
        point = Point3D(int(p[0]), int(p[1]), int(p[2]))
        current_scanner.append(point)
    if current_scanner:
        scanners.append((len(scanners), current_scanner))
    return scanners


def possible_rotated_beacons(scanner: List[Point3D]):
    mappings_rot = [
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
        [[1, 0, 0], [0, -1, 0], [0, 0, -1]],
        [[1, 0, 0], [0, 0, 1], [0, -1, 0]],
        [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
        [[-1, 0, 0], [0, 0, 1], [0, 1, 0]],
        [[-1, 0, 0], [0, 1, 0], [0, 0, -1]],
        [[-1, 0, 0], [0, 0, -1], [0, -1, 0]],
        [[0, 1, 0], [-1, 0, 0], [0, 0, 1]],
        [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
        [[0, 1, 0], [1, 0, 0], [0, 0, -1]],
        [[0, 1, 0], [0, 0, -1], [-1, 0, 0]],
        [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
        [[0, -1, 0], [0, 0, 1], [-1, 0, 0]],
        [[0, -1, 0], [-1, 0, 0], [0, 0, -1]],
        [[0, -1, 0], [0, 0, -1], [1, 0, 0]],
        [[0, 0, 1], [0, 1, 0], [-1, 0, 0]],
        [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
        [[0, 0, 1], [0, -1, 0], [1, 0, 0]],
        [[0, 0, 1], [-1, 0, 0], [0, -1, 0]],
        [[0, 0, -1], [0, 1, 0], [1, 0, 0]],
        [[0, 0, -1], [-1, 0, 0], [0, 1, 0]],
        [[0, 0, -1], [0, -1, 0], [-1, 0, 0]],
        [[0, 0, -1], [1, 0, 0], [0, -1, 0]],
    ]
    return (
        (m, [beacon.rotate(m) for beacon in scanner])
        for m in mappings_rot
    )


def place_scanner_and_probes(aligned_beacons: Dict[Point3D, Set[Point3D]], aligned_scanners: List[Point3D],
                             scanner: Scanner, print_debug: bool) -> bool:
    """
    probes is a list of already aligned probes (initially: from scanner0)
    then we try to match probes in scanner. If we find at least 12 matches, then we accept the
    rotation/translation and we add the probes, and we return "ok"
    if no one matches, then we return "failed" -- the scanner should be tried again later.

    To match:
    - For each aligned probe, we maintain a set of *all** neighbours with relative distance
    - For each probe in the scanner, we build a similar set
    - Then we check if **any** of the intersections contains at least 12 elements
    - if found, we add the new probes to all existing neighbours
    """
    for mapping, scanner_beacons in possible_rotated_beacons(scanner[1]):
        relative_beacons = [(beacon, {b - beacon for b in scanner_beacons}) for beacon in scanner_beacons]
        for aligned_beacon, relative_to_aligned in aligned_beacons.items():
            for beacon_from_scanner, scanner_and_beacon_relative_aligned_beacons in relative_beacons:
                common_beacons = relative_to_aligned & scanner_and_beacon_relative_aligned_beacons
                if len(common_beacons) >= 4:
                    scanner_position = aligned_beacon - beacon_from_scanner
                    aligned_scanners.append(scanner_position)
                    if print_debug:
                        print(f"Aligned scanner {scanner[0]} at position {scanner_position}, "
                              f"using {len(common_beacons)} common probes and rotation {mapping}")
                    # Get the "absolute" position of each beacon
                    new_beacons_absolute_pos = [
                        b + aligned_beacon
                        for b in scanner_and_beacon_relative_aligned_beacons
                    ]
                    # Add the new beacons to the aligned, with distance to all other already aligned
                    already_aligned = list(aligned_beacons.keys())
                    for new_beacon in new_beacons_absolute_pos:
                        aligned_beacons[new_beacon] = {b - new_beacon for b in already_aligned}
                    # Add the new beacons to the neighbour list of each of the existing
                    for beacon, neighbours in aligned_beacons.items():
                        new_neighbours = {b - beacon for b in new_beacons_absolute_pos}
                        neighbours.update(new_neighbours)
                    # all done, mission complete
                    return True
    return False


def get_aligned_probes(scanners, print_result):
    if get_aligned_probes.cache is None:
        # The initial state sees the first probe as "aligned" and all others as not aligned
        aligned_probes = {
            beacon: {b - beacon for b in scanners[0][1]}
            for beacon in scanners[0][1]
        }
        aligned_scanners = [Point3D(0, 0, 0)]
        unaligned_scanners = scanners[1:]
        if print_result:
            print(f"Aligned scanner at position {Point3D(0, 0, 0)}, using rotation [[1, 0, 0], [0, 1, 0], [0, 0, 1]]")
        while unaligned_scanners:
            previous_state = len(unaligned_scanners)
            if print_result:
                print(f"Scanners still left: {previous_state}")
            unaligned_scanners = [
                scanner
                for scanner in unaligned_scanners
                if not place_scanner_and_probes(aligned_probes, aligned_scanners, scanner, print_result)
            ]
            if len(unaligned_scanners) == previous_state:
                if print_result:
                    print("Error: no solution found")
                return {}, aligned_scanners
        get_aligned_probes.cache = aligned_probes, aligned_scanners
    return get_aligned_probes.cache


get_aligned_probes.cache = None


def part_1(print_result: bool = True) -> int:
    scanners = parse_data()
    aligned_probes = get_aligned_probes(scanners, print_result)[0]
    return len(aligned_probes)


def part_2(print_result: bool = True) -> int:
    scanners = parse_data()
    aligned_scanners = get_aligned_probes(scanners, print_result)[1]
    distances = []
    for p1, p2 in itertools.combinations(aligned_scanners, 2):
        dx = abs(max(p1.x, p2.x) - min(p1.x, p2.x))
        dy = abs(max(p1.y, p2.y) - min(p1.y, p2.y))
        dz = abs(max(p1.z, p2.z) - min(p1.z, p2.z))
        distances.append(dx + dy + dz)
    return max(distances)


SOLUTION_1 = 315
SOLUTION_2 = 13192

IS_SOLUTION_1_SLOW = True
IS_SOLUTION_2_SLOW = True

if __name__ == "__main__":
    print(part_1())
    print(part_2())
