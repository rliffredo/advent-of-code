from typing import Tuple, Sequence

from common import read_data, pairwise


def parse_data():
    boarding_passes = read_data("05", True)
    seats = [get_seat(boarding_pass) for boarding_pass in boarding_passes]
    seat_ids = [get_seat_id(seat) for seat in seats]
    return seat_ids


BASE_2_MAP = {"F": "0", "B": "1", "L": "0", "R": "1"}


def get_seat_id(seat: Tuple[int, int]) -> int:
    return seat[0] * 8 + seat[1]


def get_seat(boarding_pass: str) -> Tuple[int, int]:
    row = boarding_pass_coordinates(boarding_pass[:7])
    column = boarding_pass_coordinates(boarding_pass[7:])
    return row, column


def boarding_pass_coordinates(boarding_pass_coord: str):
    coord_str = "".join(BASE_2_MAP[char] for char in boarding_pass_coord)
    coord = int(coord_str, 2)
    return coord


def part_1(print_result: bool = True) -> int:
    seat_ids = parse_data()
    max_seat_id = max(seat_ids)
    if print_result:
        print(f"The max seat ID is {max_seat_id}")
    return max_seat_id


def missing(seat_ids: Sequence[int]) -> int:
    for seat_pair in pairwise(sorted(seat_ids)):
        if seat_pair[1] != seat_pair[0] + 1:
            return seat_pair[0] + 1


def part_2(print_result: bool = True) -> int:
    seat_ids = parse_data()
    missing_seat_id = missing(seat_ids)
    if print_result:
        print(f"The missing seat ID is {missing_seat_id}")
    return missing_seat_id


SOLUTION_1 = 976
SOLUTION_2 = 685

if __name__ == "__main__":
    part_1()
    part_2()
