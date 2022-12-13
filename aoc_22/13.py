import json
from functools import cmp_to_key
from itertools import chain

from common import read_line_groups


def parse_data():
    packet_pairs_str = read_line_groups('13')
    return [(json.loads(p[0]), json.loads(p[1])) for p in packet_pairs_str]


def check_pair_element(left: int | list, right: int | list) -> int:
    def cmp(a, b):
        return (a > b) - (a < b)

    if isinstance(left, int) and isinstance(right, int):
        return cmp(left, right)

    left = [left] if isinstance(left, int) else left
    right = [right] if isinstance(right, int) else right

    comparison_result = 0
    for elem_left, elem_right in zip(left, right):
        comparison_result = check_pair_element(elem_left, elem_right)
        if comparison_result != 0:
            break

    return cmp(len(left), len(right)) if comparison_result == 0 else comparison_result


def part_1(print_result: bool = True) -> int:
    packets_pair = parse_data()
    return sum(
        i + 1
        for i, pair in enumerate(packets_pair)
        if check_pair_element(pair[0], pair[1]) == -1
    )


def part_2(print_result: bool = True) -> int:
    all_packets = [[[2]], [[6]]]
    all_packets.extend(chain.from_iterable(parse_data()))
    sorted_packets = sorted(all_packets, key=cmp_to_key(check_pair_element))
    index_1 = sorted_packets.index([[2]]) + 1
    index_2 = sorted_packets.index([[6]]) + 1
    return index_1 * index_2


SOLUTION_1 = 6187
SOLUTION_2 = 23520

if __name__ == '__main__':
    print(part_1())
    print(part_2())
