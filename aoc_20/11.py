from enum import Enum
from typing import Tuple, Dict, Optional, List, Callable

from common import read_data


class SeatState(str, Enum):
    OCCUPIED = "#"
    FREE = "L"
    FLOOR = "."


SeatPos = Tuple[int, int]


class Seat:
    def __init__(self, position: SeatPos, state: str, all_neighbours: List[SeatPos] = None):
        self.position = position
        self.state = SeatState(state)
        self.all_neighbours: List[SeatPos] = all_neighbours if all_neighbours else []

    def copy_with_new_state(self, new_state: SeatState):
        return Seat(self.position, new_state, all_neighbours=self.all_neighbours)


SeatMap = Dict[SeatPos, Seat]


def load_seat_map(update_seat_neighbours: Callable[[Seat, SeatMap], None]) -> SeatMap:
    raw_data = read_data("11", True)
    seat_map = {(x, y): Seat((x, y), chair)
                for y, row in enumerate(raw_data)
                for x, chair in enumerate(row)}
    for seat in seat_map.values():
        update_seat_neighbours(seat, seat_map)
    return seat_map


def seat_tick(seat: Seat, threshold: int, seat_map: SeatMap) -> Seat:
    if seat.state is SeatState.FLOOR:  # small performance optimization :)
        return seat
    occupied_around = sum(1 for adj in seat.all_neighbours if seat_map[adj].state is SeatState.OCCUPIED)
    if seat.state is SeatState.FREE and occupied_around == 0:
        return seat.copy_with_new_state(SeatState.OCCUPIED)
    if seat.state is SeatState.OCCUPIED and occupied_around >= threshold:
        return seat.copy_with_new_state(SeatState.FREE)
    return seat


def map_tick(seat_map: SeatMap, threshold: int) -> SeatMap:
    return {seat_pos: seat_tick(seat, threshold, seat_map) for seat_pos, seat in seat_map.items()}


def predict_free_seats(seat_map, threshold):
    old_seat_map = {}
    while seat_map != old_seat_map:
        old_seat_map = seat_map.copy()
        seat_map = map_tick(seat_map, threshold)
    free_seats = sum(1 for seat in seat_map.values() if seat.state is SeatState.OCCUPIED)
    return free_seats


def immediate_neighbours(seat: Seat, seat_map: SeatMap) -> None:
    neighbours = [(seat.position[0] + dx, seat.position[1] + dy)
                  for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                  if (dx, dy) != (0, 0)]
    seat.all_neighbours = [neighbour for neighbour in neighbours if neighbour in seat_map]


def part_1(print_result: bool = True) -> int:
    seat_map = load_seat_map(immediate_neighbours)
    free_seats = predict_free_seats(seat_map, threshold=4)
    if print_result:
        print(f"At the end, there are {free_seats} occupied seats (method 1)")
    return free_seats


def visible_neighbours(seat: Seat, seat_map: SeatMap) -> None:
    def get_first_neighbour(position: SeatPos, dx: int, dy: int) -> Optional[Seat]:
        position = (position[0] + dx, position[1] + dy)
        while position in seat_map:
            if seat_map[position].state != SeatState.FLOOR:
                return seat_map[position]
            position = (position[0] + dx, position[1] + dy)
        return None

    neighbours = [
        get_first_neighbour(seat.position, dx, dy)
        for dx in (-1, 0, 1) for dy in (-1, 0, 1)
        if (dx, dy) != (0, 0)
    ]
    seat.all_neighbours = [neighbour.position for neighbour in neighbours if neighbour]


def part_2(print_result: bool = True) -> int:
    seat_map = load_seat_map(visible_neighbours)
    free_seats = predict_free_seats(seat_map, threshold=5)
    if print_result:
        print(f"At the end, there are {free_seats} occupied seats (method 2)")
    return free_seats


SOLUTION_1 = 2494
SOLUTION_2 = 2306

if __name__ == "__main__":
    part_1()
    part_2()
