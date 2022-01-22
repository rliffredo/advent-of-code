import statistics

from common import read_data


def parse_data():
    raw_data = read_data("07", False)
    return [int(n) for n in raw_data.split(",")]


def part_1(print_result: bool = True) -> int:
    data = parse_data()
    best_pos = int(statistics.median(data))
    return sum(abs(n - best_pos) for n in data)


def calc_fuel(data, candidate_pos):
    n = abs(data - candidate_pos)
    return n * (n + 1) // 2


def part_2(print_result: bool = True) -> int:
    data = parse_data()
    min_pos = min(data)
    max_pos = max(data)
    fuel_costs = [sum(calc_fuel(n, candidate_pos) for n in data) for candidate_pos in range(min_pos, max_pos + 1)]
    return min(fuel_costs)


SOLUTION_1 = 326132
SOLUTION_2 = 88612508

if __name__ == "__main__":
    print(part_1())
    print(part_2())
