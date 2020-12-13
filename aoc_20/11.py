from enum import Enum
from typing import Tuple, Dict, Optional, List, Callable

from common import read_data


class SeatState(str, Enum):
    OCCUPIED = "#"
    FREE = "L"
    FLOOR = "."


SeatPos = Tuple[int, int]


class Seat:
    __slots__ = ['position', 'state', 'all_neighbours', 'next_state', 'occupied_neighbours', 'next_occupied_neighbours',
                 'threshold', 'hash_', 'cluster']

    def __init__(self, position: SeatPos, state: str, threshold: int):
        self.hash_ = hash(position)
        self.position = position
        self.all_neighbours: List[Seat] = []
        self.cluster: List[Seat] = []
        self.state = SeatState(state)
        self.next_state = None
        self.occupied_neighbours = 0
        self.threshold = threshold
        self.next_occupied_neighbours = 0

    def set_neighbours(self, neighbours: List[Optional['Seat']]) -> None:
        self.all_neighbours = [n for n in neighbours if n is not None]
        self.cluster = self.all_neighbours + [self]

    def set_occupied(self) -> None:
        self.next_state = SeatState.OCCUPIED
        for adj in self.all_neighbours:
            adj.next_occupied_neighbours += 1

    def set_empty(self) -> None:
        self.next_state = SeatState.FREE
        for adj in self.all_neighbours:
            adj.next_occupied_neighbours -= 1

    def should_change_to_occupied(self) -> bool:
        return self.state is SeatState.FREE and self.occupied_neighbours == 0

    def should_change_to_free(self) -> bool:
        return self.state is SeatState.OCCUPIED and self.occupied_neighbours >= self.threshold

    def next_generation(self) -> None:
        self.state = self.next_state
        self.occupied_neighbours = self.next_occupied_neighbours


SeatMap = Dict[SeatPos, Seat]


def load_seat_map(update_seat_neighbours: Callable[[Seat, SeatMap], None], threshold) -> SeatMap:
    raw_data = read_data("11", True)
    seat_map = {(x, y): Seat((x, y), chair, threshold)
                for y, row in enumerate(raw_data)
                for x, chair in enumerate(row)}
    for seat in seat_map.values():
        update_seat_neighbours(seat, seat_map)
    return seat_map


def seat_tick(seat: Seat) -> bool:
    if seat.should_change_to_occupied():
        seat.set_occupied()
        return True
    if seat.should_change_to_free():
        seat.set_empty()
        return True
    return False


def predict_free_seats(seat_map: SeatMap) -> int:
    changed_nodes = seat_map
    while changed_nodes:
        seats_to_recalc = list(changed_nodes.values())
        changed_nodes = {}
        # First phase: calculate next state of nodes
        for seat in seats_to_recalc:
            seat_has_changed = seat_tick(seat)
            if not seat_has_changed:
                continue
            for node_to_refresh in seat.cluster:
                changed_nodes[node_to_refresh.hash_] = node_to_refresh
        # Second phase: update state to what was calculated
        for seat in seats_to_recalc:
            seat.next_generation()

    free_seats = sum(1 for seat in seat_map.values() if seat.state is SeatState.OCCUPIED)
    return free_seats


def immediate_neighbours(seat: Seat, seat_map: SeatMap) -> None:
    neighbours = [(seat.position[0] + dx, seat.position[1] + dy)
                  for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                  if (dx, dy) != (0, 0)]
    seat.set_neighbours([seat_map[neighbour] for neighbour in neighbours if neighbour in seat_map])


def part_1(print_result: bool = True) -> int:
    seat_map = load_seat_map(immediate_neighbours, 4)
    free_seats = predict_free_seats(seat_map)
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
    seat.set_neighbours(neighbours)


def part_2(print_result: bool = True) -> int:
    seat_map = load_seat_map(visible_neighbours, 5)
    free_seats = predict_free_seats(seat_map)
    if print_result:
        print(f"At the end, there are {free_seats} occupied seats (method 2)")
    return free_seats


SOLUTION_1 = 2494
SOLUTION_2 = 2306

if __name__ == "__main__":
    part_1()
    part_2()
