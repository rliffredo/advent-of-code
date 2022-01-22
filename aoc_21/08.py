import itertools
from dataclasses import dataclass
from typing import List

from common import read_data


@dataclass
class DisplayAnalysis:
    signals: List[str]
    digits: List[str]


def parse_data():
    raw_data_lines = read_data("08", True)
    raw_signals_and_digits = [line.split("|") for line in raw_data_lines]
    signals_and_digits = [DisplayAnalysis(rsi.split(), rse.split()) for rsi, rse in raw_signals_and_digits]
    return signals_and_digits


def part_1(print_result: bool = True) -> int:
    displays = parse_data()
    # we just need to count the digits that can be mapped to 1, 4, 7, 8
    all_digits = itertools.chain.from_iterable(display.digits for display in displays)
    digits_1478 = [segment for segment in all_digits if len(segment) in (2, 3, 4, 7)]
    return len(digits_1478)


def map_digit(signal, segment_map):
    mapped_digit = "".join(sorted("abcdefg"[segment_map.index(segment)] for segment in signal))
    digit_map = {
        "abcefg": 0,
        "cf": 1,
        "acdeg": 2,
        "acdfg": 3,
        "bcdf": 4,
        "abdfg": 5,
        "abdefg": 6,
        "acf": 7,
        "abcdefg": 8,
        "abcdfg": 9
    }
    return digit_map.get(mapped_digit, -1)


def make_number(digits, segment_map):
    p = 1
    r = 0
    for digit in digits[::-1]:
        r += map_digit(digit, segment_map) * p
        p *= 10
    return r


def decode_display(display):
    # Check every possible permutation, to see if it maps to something. If all digits map to a result, then
    # we have found a solution.
    for segment_map in itertools.permutations("abcdefg", 7):
        if all(map_digit(signal, segment_map) != -1 for signal in display.signals):
            break
    else:
        assert False, "We must find a valid mapping!"
    return make_number(display.digits, segment_map)


def part_2(print_result: bool = True) -> int:
    displays = parse_data()
    numbers = [decode_display(display) for display in displays]
    return sum(numbers)


SOLUTION_1 = 387
SOLUTION_2 = 986034

if __name__ == "__main__":
    print(part_1())
    print(part_2())
