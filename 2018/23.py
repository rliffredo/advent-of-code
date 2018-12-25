import heapq
import math
import re
from collections import namedtuple
from typing import List, Union

Sphere = namedtuple('Sphere', 'x, y, z, r, id')


def parse_line(line: str):
    # pos=<1,3,1>, r=1
    m = re.match(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)', line)
    try:
        return tuple(map(int, m.groups()))
    except TypeError:
        print(line)
        raise


def parse_file():
    data = open('input_23.txt').readlines()
    parsed_data = [parse_line(d) for d in data]
    nanobots = [Sphere(x=t[0], y=t[1], z=t[2], r=t[3], id=i) for i, t in enumerate(parsed_data)]
    return nanobots


def distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)


def count_in_range_of_strongest(nanobots: List[Sphere]):
    max_nanobot = max(nanobots, key=lambda s: s.r)
    in_range = [nanobot for nanobot in nanobots if distance(nanobot, max_nanobot) <= max_nanobot.r]
    return len(in_range)


nanobots_ = parse_file()
print(f'There are {count_in_range_of_strongest(nanobots_)} in range of the strongest')

########

# Algorithm adapted from https://raw.githack.com/ypsu/experiments/master/aoc2018day23/vis.html

Point = namedtuple('Point', 'x ,y, z')

class Box:
    def __init__(self, top_left: Point, size: int, nanobots: List[Sphere]):
        if int(size / 2) != size // 2:
            size = int(math.ceil(size / 2) * 2)
        self.size = size
        self.top_left = top_left
        self.bots_in_range = []
        for bot in nanobots:
            if self._distance_from_point(bot) <= bot.r:
                self.bots_in_range.append(bot)
        self.nanobots = nanobots

    @property
    def distance_from_origin(self) -> int:
        return self._distance_from_point(Point(0, 0, 0))

    def _distance_from_point(self, point: Union[Point, Sphere]) -> int:

        def dist_axis(v1, v2, p):
            if v1 <= p <= v2:
                return 0
            return min(abs(v1 - p), abs(v2 - p))

        x = dist_axis(self.top_left.x, self.top_left.x + self.size - 1, point.x)
        y = dist_axis(self.top_left.y, self.top_left.y + self.size - 1, point.y)
        z = dist_axis(self.top_left.z, self.top_left.z + self.size - 1, point.z)
        dist = x + y + z
        return dist

    def get_sub_boxes(self) -> List['Box']:
        if self.size == 1:
            return [self]

        assert int(self.size / 2) == self.size // 2, 'Size is always a multiple of two'

        sub_size = self.size // 2
        box_points = [Point(self.top_left.x + x * sub_size,
                            self.top_left.y + y * sub_size,
                            self.top_left.z + z * sub_size)
                      for x in (0, 1) for y in (0, 1) for z in (0, 1)]
        return [Box(point, sub_size, self.nanobots) for point in box_points]

    def __lt__(self, other):
        t_self = -len(self.bots_in_range), self.distance_from_origin, self.size
        t_other = -len(other.bots_in_range), other.distance_from_origin, other.size
        return t_self < t_other

    def __eq__(self, other):
        if not isinstance(other, Box):
            return False
        return self.size == other.size and self.top_left == other.top_left

    def __str__(self):
        return f'Box {self.top_left}/{self.size}/{len(self.bots_in_range)}'


def get_initial_box(nanobots):
    def box_in_dimension(dimension):
        min_d = min(getattr(b, dimension) - b.r for b in nanobots)
        max_d = max(getattr(b, dimension) + b.r + 1 for b in nanobots)
        size_d = 2 ** (math.ceil(math.log2(abs(max_d - min_d))))
        return min_d, size_d

    min_x, size_x = box_in_dimension('x')
    min_y, size_y = box_in_dimension('y')
    min_z, size_z = box_in_dimension('z')
    size_box = max(size_x, size_y, size_z)

    box = Box(Point(min_x, min_y, min_z), size_box, nanobots)
    return box


def find_nearest_box(nanobots) -> Box:
    boxes_to_analyze = []
    initial_box = get_initial_box(nanobots)
    heapq.heappush(boxes_to_analyze, initial_box)
    while boxes_to_analyze:
        box = heapq.heappop(boxes_to_analyze)
        if box.size == 1:
            return box
        for sub_box in box.get_sub_boxes():
            heapq.heappush(boxes_to_analyze, sub_box)

    assert False, 'Always finish by finding a box of size 1'


print(f'Distance from origin is {find_nearest_box(nanobots_).distance_from_origin}')
