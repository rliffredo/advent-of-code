import math

import networkx as nx

from common import read_data


def parse_data():
    raw_data = read_data("09", True)
    return {(x, y): int(char) for y, line in enumerate(raw_data) for x, char in enumerate(line)}


def is_low_point(x, y, height_map):
    return all(
        height_map.get((x + dx, y + dy), 10) > height_map[x, y]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, +1)]
    )


def part_1(print_result: bool = True) -> int:
    height_map = parse_data()
    return sum(
        h + 1
        for (x, y), h in height_map.items()
        if is_low_point(x, y, height_map)
    )


def part_2(print_result: bool = True) -> int:
    height_map = parse_data()
    basins = build_basin_forest(height_map)
    split_basins = {
        tuple(sorted(nx.algorithms.components.node_connected_component(basins, (p))))
        for p in basins
    }
    basin_sizes = [len(b) for b in split_basins]
    top_basins = sorted(basin_sizes)[-3:]
    return math.prod(top_basins)


def build_basin_forest(height_map):
    g = nx.Graph()
    for (x, y), h in height_map.items():
        g.add_node((x, y))
        if h == 9:
            continue
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, +1)]:
            if height_map.get((x + dx, y + dy), 10) < 9:
                g.add_edge((x, y), (x + dx, y + dy))
    return g


SOLUTION_1 = 588
SOLUTION_2 = 964712

if __name__ == "__main__":
    print(part_1())
    print(part_2())
