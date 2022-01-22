from itertools import tee

from common import read_data, pairwise


def parse_data():
    raw_numbers = read_data("01", True)
    return [int(n) for n in raw_numbers]


def part_1(print_result: bool = True) -> int:
    depths = parse_data()
    measurement_pairs = list(pairwise(depths))
    increased_pairs = [p for p in measurement_pairs if p[1] > p[0]]
    increased = len(increased_pairs)
    return increased


def thricewise(iterable):
    """
    s -> (s0,s1,s2), (s1,s2), (s2, s3), ...
    """
    a, b, c = tee(iterable, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)


def part_2(print_result: bool = True) -> int:
    depths = parse_data()
    sliding_windows = list(sum(t) for t in thricewise(depths))
    measurement_pairs = list(pairwise(sliding_windows))
    increased_pairs = [p for p in measurement_pairs if p[1] > p[0]]
    increased = len(increased_pairs)
    return increased


SOLUTION_1 = 1400
SOLUTION_2 = 1429

if __name__ == "__main__":
    print(part_1())
    print(part_2())

