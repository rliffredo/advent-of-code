import heapq
from collections import namedtuple
from dataclasses import dataclass
from enum import IntEnum
from typing import Dict, List, Tuple, Set



Point = namedtuple('Point', 'x, y')


class RegionType(IntEnum):
    rocky = 0
    wet = 1
    narrow = 2

    def __str__(self) -> str:
        if self.value == RegionType.rocky:
            return '.'
        elif self.value == RegionType.wet:
            return '='
        else:  # RegionType.narrow
            return '|'


class Cave:
    def __init__(self, depth, target_position: Point, grid = None):
        self.gi_cache: Dict[Point, int] = {
            Point(0, 0): 0,
            target_position: 0,
        }
        self.depth = depth
        self.target_position = target_position
        self.el_cache: Dict[Point, int] = {}
        self.grid = grid
        # (x, y) -> geologic index, erosion level, risk

    def geologic_index(self, point: Point) -> int:
        if self.grid:
            return self.grid[(point.x, point.y)][0]

        if point not in self.gi_cache:
            if point.y == 0:
                self.gi_cache[point] = point.x * 16807
            elif point.x == 0:
                self.gi_cache[point] = point.y * 48271
            else:
                el_left = self.erosion_level(Point(point.x - 1, point.y))
                el_up = self.erosion_level(Point(point.x, point.y - 1))
                self.gi_cache[point] = el_left * el_up
        return self.gi_cache[point]

    def erosion_level(self, point: Point) -> int:
        if self.grid:
            return self.grid[(point.x, point.y)][1]

        if point not in self.el_cache:
            gi_index = self.geologic_index(point) + self.depth
            self.el_cache[point] = gi_index % 20183
        return self.el_cache[point]

    def region_type(self, point: Point) -> RegionType:
        return RegionType(self.erosion_level(point) % 3)

    def print(self):
        def region_value(point: Point):
            return str(self.region_type(point)) if point != self.target_position else 'X'

        table = [
            [region_value(Point(x, y)) for x in range(self.target_position.x + 10)]
            for y in range(self.target_position.y + 10)
        ]
        lines = []
        for i, line in enumerate(table):
            lines.append(''.join(c for c in line))
        res = '\n'.join(lines) + '\n'
        print(res)


test = False

if test:
    DEPTH = 510
    TARGET = Point(10, 10)
else:
    # DEPTH = 11541
    # TARGET = Point(14, 778)
    DEPTH = 11541
    TARGET = Point(14, 250)


def make_cave(depth, target, grid):
    cave = Cave(depth, target, grid)
    cave.print()
    return cave


def get_risk_level(cave, target):
    points = [Point(x, y) for x in range(target.x + 1) for y in range(target.y + 1)]
    total_risk_level = sum(cave.region_type(p) for p in points)
    return total_risk_level


grid = verify.generate_grid(DEPTH, (TARGET.x+150, TARGET.y+150))
cave_ = make_cave(DEPTH, TARGET, grid)
# print(f'Risk level is: {get_risk_level(cave_, TARGET)}')

#############

class Tool(IntEnum):
    torch = 0
    gear = 1
    nothing = 2


PointWithTool = namedtuple('PointWithTool', 'x, y, tool')


@dataclass
class QueueElement:
    node: PointWithTool
    time_to_reach: int
    path_so_far: List[Tuple[str, Point, int, Tool, RegionType]]

    def __lt__(self, other: 'QueueElement'):
        return self.time_to_reach < other.time_to_reach

    def __eq__(self, other: 'QueueElement'):
        return self.node == other.node


def find_shortest_path(cave: Cave, start: Point, target: Point) -> Tuple[int, QueueElement]:
    min_full_path: QueueElement = None
    regions_visited: Dict[PointWithTool, int] = {}
    regions_to_visit: List[QueueElement] = []
    heapq.heappush(regions_to_visit, QueueElement(node=PointWithTool(*start, Tool.torch),
                                                  time_to_reach=0,
                                                  path_so_far=[]))
    min_path = 500000
    while len(regions_to_visit) > 0:
        cr = heapq.heappop(regions_to_visit)  # type: QueueElement
        if cr.node in regions_visited:
            continue
        regions_visited[cr.node] = cr.time_to_reach

        if cr.node.x == target.x and cr.node.y == target.y:
            cost = cr.time_to_reach
            if cr.node.tool != Tool.torch:
                cost += 7
            if cost < min_path:
                min_full_path = cr
                min_path = cost
            continue

        neighbours = {
            Point(cr.node.x, cr.node.y - 1): "Up",
            Point(cr.node.x - 1, cr.node.y): "Left",
            Point(cr.node.x + 1, cr.node.y): "Right",
            Point(cr.node.x, cr.node.y + 1): "Down",
        }
        neighbours_with_tool: Set[Tuple[Point, int, Tool]] = set()
        for neighbour in neighbours:
            if neighbour.x < 0 or neighbour.y < 0:
                continue

            if neighbour.x > 100 or neighbour.y > 400:
                continue

            options = get_move_options(cave, neighbour, target, cr.node.tool)
            neighbours_with_tool.update(options)

        for neighbour, cost, tool in neighbours_with_tool:
            time_to_reach_neighbour = cr.time_to_reach + cost
            if time_to_reach_neighbour > min_path:  # heuristic to cut the calculation down
                continue

            point_with_tool = PointWithTool(*neighbour, tool)
            if point_with_tool in regions_visited and regions_visited[point_with_tool] < time_to_reach_neighbour:
                continue

            path = [p for p in cr.path_so_far]
            path_element = neighbours[neighbour], neighbour, cost, tool, cave.region_type(neighbour)
            path.append(path_element)
            node_to_visit = QueueElement(node=point_with_tool,
                                         time_to_reach=time_to_reach_neighbour,
                                         path_so_far=path)
            heapq.heappush(regions_to_visit, node_to_visit)

    return min_path, min_full_path


def get_move_cost(current_tool: Tool, new_tool: Tool):
    return 1 if current_tool == new_tool else 8


def get_move_options(cave: Cave, point: Point, target: Point, current_tool: Tool) -> Set[Tuple[Point, int, Tool]]:
    tools_for_region = {
        RegionType.rocky: [Tool.torch, Tool.gear],
        RegionType.wet: [Tool.gear, Tool.nothing],
        RegionType.narrow: [Tool.nothing, Tool.torch],
    }
    to_region_type = cave.region_type(point) if point != target else RegionType.rocky
    new_region_tools = tools_for_region[to_region_type]
    return {(point, get_move_cost(current_tool, new_tool), new_tool) for new_tool in new_region_tools}


def print_path(cave: Cave, path: List[Tuple[str, Point, int, Tool, RegionType]] = None):
    def region_value(point: Point, path):
        if point in path:
            return '*'
        if point == cave.target_position:
            return 'X'
        return str(cave.region_type(point))

    path_points = {p[1] for p in path}
    table = [
        [region_value(Point(x, y), path_points) for x in range(cave.target_position.x + 10)]
        for y in range(cave.target_position.y + 10)
    ]
    lines = []
    for i, line in enumerate(table):
        lines.append(''.join(c for c in line))
    res = '\n'.join(lines) + '\n'
    print(res)


min_path, min_path_info = find_shortest_path(cave_, Point(0, 0), TARGET)

print(f'Minumum time required is {min_path}')

# 1071 too high
# 1064 too low


# Risk level is: 11575
# Found path at cost 1071
# Found path at cost 1064
# Found path at cost 1073
# Found path at cost 1066
# Found path at cost 1071
# Found path at cost 1071
# Found path at cost 1071
# Found path at cost 1071
# Found path at cost 1078
# Found path at cost 1064
# Minumum time required is 1064


# 1065 too low
# 1066 / 1067 /

# 1068
