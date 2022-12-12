import networkx as nx

from common import read_data


def parse_map():
    lines = read_data("12", True)
    height_map = {
        (x, y): c
        for (y, line) in enumerate(lines)
        for (x, c) in enumerate(line)
        }
    start_point = next(p for p, h in height_map.items() if h == 'S')
    end_point = next(p for p, h in height_map.items() if h == 'E')
    height_map[start_point] = 'a'
    height_map[end_point] = 'z'
    return height_map, start_point, end_point


def make_access_map(height_map):
    access_map = nx.DiGraph()
    for current_point, current_height in height_map.items():
        x, y = current_point
        neighbours = [n for n in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if n in height_map]
        for neighbour in neighbours:
            neighbour_height = height_map[neighbour]
            delta_height = ord(neighbour_height) - ord(current_height)
            if delta_height <= 1:
                access_map.add_edge(current_point, neighbour)
    return access_map


def part_1(print_result: bool = True) -> int:
    height_map, start_point, end_point = parse_map()
    access_map = make_access_map(height_map)
    return nx.shortest_path_length(access_map, start_point, end_point)


def part_2(print_result: bool = True) -> int:
    height_map, _, end_point = parse_map()
    access_map = make_access_map(height_map)
    paths = nx.shortest_path_length(access_map, target=end_point)
    return min(steps for source, steps in paths.items() if height_map[source] == 'a')


SOLUTION_1 = 425
SOLUTION_2 = 418

if __name__ == "__main__":
    print(part_1())
    print(part_2())
