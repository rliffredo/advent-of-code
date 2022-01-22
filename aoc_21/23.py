import heapq
import itertools
from typing import Literal

from common import read_data

room_idx = {"A": 2, "B": 4, "C": 6, "D": 8}
MOVE_COST = {"A": 1, "B": 10, "C": 100, "D": 1000}

Amphipods = Literal['A', 'B', 'C', 'D']


class State:
    @staticmethod
    def from_string_data(room_a, room_b, room_c, room_d) -> 'State':
        return State(
            hallway={},
            rooms={
                "A": [c for c in room_a[::-1]],
                "B": [c for c in room_b[::-1]],
                "C": [c for c in room_c[::-1]],
                "D": [c for c in room_d[::-1]],
            },
            cost=0,
            room_size=len(room_a)
        )

    def __init__(self, hallway, rooms, cost, room_size, previous_states=None):
        self.hallway = hallway
        self.rooms = rooms
        self.cost = cost
        self.room_size = room_size
        self.previous_states = previous_states if previous_states else []

        self._room_str = {
            k: "".join([str(c) for c in v]).ljust(self.room_size, ".")
            for k, v in self.rooms.items()
        }
        hh = "".join(self.hallway.get(n, '.') for n in range(11))
        hr = "".join(self._room_str["A"] + self._room_str["B"] + self._room_str["C"] + self._room_str["D"])
        self._state_hash = hash(hh + hr)

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        assert isinstance(other, State)
        return self._state_hash == other._state_hash

    def __hash__(self):
        return self._state_hash

    def available_room_moves(self):
        moves = []
        # Try to move out items that are already in the hallway
        for room_type, room in self.rooms.items():
            if not room:
                continue
            if all(r == room_type for r in room):
                continue
            positions = self.hallway_positions_from_room(room_type)
            moves += [(room_type, pos) for pos in positions]
        return moves

    def available_hallway_moves(self):
        # Try to move in items that do not block others
        return [
            (position, amp)
            for position, amp in self.hallway.items()
            if self.can_position_reach_room(position, amp)
        ]

    def hallway_positions_from_room(self, room_type):
        base_position = room_idx[room_type]
        left_positions = itertools.takewhile(lambda i: i not in self.hallway, range(base_position, -1, -1))
        right_positions = itertools.takewhile(lambda i: i not in self.hallway, range(base_position + 1, 11))
        return [p for p in itertools.chain(left_positions, right_positions) if p not in room_idx.values()]

    def can_position_reach_room(self, hallway_position, room_type):
        if len(self.rooms[room_type]) == self.room_size:
            return False
        if any(occupant != room_type for occupant in self.rooms[room_type]):
            return False
        room_position = room_idx[room_type]
        route = range(room_position, hallway_position, 1 if hallway_position > room_position else -1)
        return all(n not in self.hallway for n in route)

    def room_to_hallway(self, room_type, pos):
        assert pos not in self.hallway
        assert self.rooms[room_type], f"Room {room_type} is never empty"
        hallway = self.hallway.copy()
        rooms = {k: v.copy() for k, v in self.rooms.items()}
        hallway[pos] = rooms[room_type].pop()
        amphipod = self.rooms[room_type][-1]
        distance = abs(room_idx[room_type] - pos)
        out_of_room_cost = self.room_size + 1 - len(self.rooms[room_type])
        move_cost = (distance + out_of_room_cost) * MOVE_COST[amphipod]
        return State(
            hallway=hallway,
            rooms=rooms,
            cost=self.cost + move_cost,
            room_size=self.room_size,
            previous_states=self.previous_states + [self]
        )

    def hallway_to_room(self, pos, room_type):
        assert pos in self.hallway
        assert len(self.rooms[room_type]) < self.room_size, f"Room {room_type} is never full"
        hallway = self.hallway.copy()
        rooms = {k: v.copy() for k, v in self.rooms.items()}
        rooms[room_type].append(hallway.pop(pos))
        in_room_cost = self.room_size - len(self.rooms[room_type])
        distance = abs(room_idx[room_type] - pos) + in_room_cost
        move_cost = distance * MOVE_COST[room_type]
        return State(
            hallway=hallway,
            rooms=rooms,
            cost=self.cost + move_cost,
            room_size=self.room_size,
            previous_states=self.previous_states + [self]
        )

    def print(self):
        def getr(room, idx):
            return self._room_str[room][idx]
        print("#############")
        print(f"#{''.join([self.hallway.get(i, '.') for i in range(11)])}#")
        top = self.room_size - 1
        print(f"###{getr('A', top)}#{getr('B', top)}#{getr('C', top)}#{getr('D', top)}###")
        for n in range(top - 1, -1, -1):
            print(f"  #{getr('A', n)}#{getr('B', n)}#{getr('C', n)}#{getr('D', n)}#  ")
        print(f"  #########  ")


def parse_data(extra_a, extra_b, extra_c, extra_d):
    lines = read_data("23", True)
    return State.from_string_data(
        lines[2][3] + extra_a + lines[3][3],
        lines[2][5] + extra_b + lines[3][5],
        lines[2][7] + extra_c + lines[3][7],
        lines[2][9] + extra_d + lines[3][9],
    )


def shortest_path(start_state, end_state, debug_output):
    seen = set()
    h = []
    heapq.heappush(h, start_state)
    while h:
        state = heapq.heappop(h)
        if state == end_state:
            # Solution found!
            if debug_output:
                print("Found solution!")
                cost = 0
                for step_no, step in enumerate(state.previous_states):
                    print(f"*******\nStep {step_no} (cost: {step.cost - cost}; total cost: {step.cost})")
                    cost = step.cost
                    step.print()
                print(f"*******\nStep {len(state.previous_states)} (cost: {state.cost - cost};"
                      f"total cost: {state.cost})")
                state.print()
            return state.cost

        if state in seen:
            # We have already analyzed this state, and it was less expensive then!
            continue
        seen.add(state)

        # states_from_room_moves
        for move in state.available_room_moves():
            heapq.heappush(h, state.room_to_hallway(*move))
        # states_from_hallway_moves
        for move in state.available_hallway_moves():
            heapq.heappush(h, state.hallway_to_room(*move))

    assert False, "We know there is a solution!"


def part_1(print_result: bool = True) -> int:
    start_state = parse_data("", "", "", "")
    end_state = State.from_string_data("AA", "BB", "CC", "DD")
    cost = shortest_path(start_state, end_state, print_result)
    return cost


def part_2(print_result: bool = True) -> int:
    start_state = parse_data("DD", "CB", "BA", "AC")
    end_state = State.from_string_data("AAAA", "BBBB", "CCCC", "DDDD")
    cost = shortest_path(start_state, end_state, print_result)
    return cost


SOLUTION_1 = 14371
SOLUTION_2 = 40941

IS_SOLUTION_1_SLOW = True
IS_SOLUTION_2_SLOW = True

if __name__ == "__main__":
    print(part_1())
    print(part_2())
