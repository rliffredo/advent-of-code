import re
from collections import defaultdict

from common import read_data, print_map


def parse_data():
    raw_line_defs = read_data("05", True)
    def_pattern = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")
    line_defs = [def_pattern.match(raw_def).groups() for raw_def in raw_line_defs]
    int_line_defs = [[int(n) for n in line_def] for line_def in line_defs]
    return [((p[0], p[1]), (p[2], p[3])) for p in int_line_defs]


def draw_lines(hv_lines_defs, include_diagonal, print_result):
    wind_map = defaultdict(int)
    for (start_x, start_y), (end_x, end_y) in hv_lines_defs:
        delta_x = end_x - start_x
        step_x = 1 if delta_x > 0 else -1
        delta_y = end_y - start_y
        step_y = 1 if delta_y > 0 else -1
        if delta_x == 0 or delta_y == 0:
            for x in range(0, delta_x + step_x, step_x):
                for y in range(0, delta_y + step_y, step_y):
                    wind_map[(start_x + x, start_y + y)] += 1
        if include_diagonal and abs(delta_x) == abs(delta_y):
            for n in range(abs(delta_y) + 1):
                wind_map[(start_x + n * step_x, start_y + n * step_y)] += 1

    if print_result:
        map_sizes = (0, max(c[0] for c in wind_map), 0, max(c[1] for c in wind_map))
        print_map(map_sizes, lambda x, y: str(wind_map[(x, y)]).replace("0", "."))

    return wind_map


def part_1(print_result: bool = True) -> int:
    line_defs = parse_data()
    wind_map = draw_lines(line_defs, False, False)
    points_with_strong_winds = len([p for p in wind_map.values() if p >= 2])
    return points_with_strong_winds


def part_2(print_result: bool = True) -> int:
    line_defs = parse_data()
    wind_map = draw_lines(line_defs, True, print_result)
    points_with_strong_winds = len([p for p in wind_map.values() if p >= 2])
    return points_with_strong_winds


SOLUTION_1 = 6710
SOLUTION_2 = 20121

if __name__ == "__main__":
    print(part_1())
    print(part_2())
