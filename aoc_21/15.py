import networkx as nx

from common import read_data, pairwise


def parse_data():
    map_lines = read_data("15", True)
    g = nx.DiGraph()
    x, y = 0, 0
    for y, line in enumerate(map_lines):
        for x, char in enumerate(line):
            add_entering_risk(g, x, y, int(char))
    exit_point = (x, y)
    return g, exit_point


def add_entering_risk(g, x, y, risk):
    g.add_edge((x - 1, y), (x, y), risk=risk)
    g.add_edge((x + 1, y), (x, y), risk=risk)
    g.add_edge((x, y - 1), (x, y), risk=risk)
    g.add_edge((x, y + 1), (x, y), risk=risk)


def get_best_path(exit_point, risk_map):
    best_path = nx.shortest_path(risk_map, source=(0, 0), target=exit_point, weight="risk")
    path_cost = sum(risk_map.get_edge_data(p1, p2)["risk"] for p1, p2 in pairwise(best_path))
    return path_cost


def part_1(print_result: bool = True) -> int:
    risk_map, exit_point = parse_data()
    path_cost = get_best_path(exit_point, risk_map)
    return path_cost


def make_full_risk_map(risk_map, lower_right, map_multiplier):
    larger_map = nx.DiGraph()
    len_x = lower_right[0] + 1
    len_y = lower_right[1] + 1
    for x in range(len_x):
        for y in range(len_y):
            original_risk = risk_map.get_edge_data((x-1, y), (x, y))["risk"]
            for mx in range(map_multiplier):
                row_risk = ((original_risk - 1 + mx) % 9) + 1
                for my in range(map_multiplier):
                    cell_risk = ((row_risk - 1 + my) % 9) + 1
                    translated_x = x + len_x * mx
                    translated_y = y + len_y * my
                    add_entering_risk(larger_map, translated_x, translated_y, cell_risk)
    return larger_map, (len_x * map_multiplier - 1, len_y * map_multiplier - 1)


def part_2(print_result: bool = True) -> int:
    risk_map, exit_point = parse_data()
    larger_map, real_exit_point = make_full_risk_map(risk_map, exit_point, 5)
    path_cost = get_best_path(real_exit_point, larger_map)
    return path_cost


SOLUTION_1 = 403
SOLUTION_2 = 2840

IS_SOLUTION_2_SLOW = True

if __name__ == "__main__":
    print(part_1())
    print(part_2())
