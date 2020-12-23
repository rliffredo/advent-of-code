import math
from dataclasses import dataclass
from time import perf_counter_ns
from typing import Tuple, Optional, List

from common import pairwise

INITIAL_CIRCLE = tuple(int(n) for n in "394618527")


@dataclass
class Cup:
    label: int
    next: Optional['Cup']

    __slots__ = ('label', 'next')

    def __repr__(self):
        return f"Cup {self.label}, [>{self.next.label if self.next else None}]"


class Circle:
    def __init__(self, cups: Tuple[int]):
        cup_circle: Tuple[Cup, ...] = tuple(Cup(label=cup - 1, next=None) for cup in cups)
        self.cup_map = {}
        next_cup = None
        for cup, next_cup in pairwise(cup_circle):
            cup.next = next_cup
            self.cup_map[cup.label] = cup
        assert next_cup
        self.cup_map[next_cup.label] = next_cup
        cup_circle[-1].next = cup_circle[0]
        self.current_cup = cup_circle[0]
        self.max_cup = max(cups)

    def pick_up_three_cups(self):
        first_cup = self.current_cup.next
        second_cup = first_cup.next
        third_cup = second_cup.next
        self.current_cup.next = third_cup.next
        return [first_cup.label, second_cup.label, third_cup.label], first_cup, third_cup

    def insert_three_cups(self, first, last, dest):
        destination = self.cup_map[dest]
        after_destination = destination.next
        destination.next = first
        last.next = after_destination

    def move_current(self):
        self.current_cup = self.current_cup.next

    def from_first(self, max_chars: int = 0) -> List[int]:
        cups = []
        first_cup = self.cup_map[0]
        current_cup = first_cup
        for _ in range(max_chars or self.max_cup):
            current_cup = current_cup.next
            if current_cup == first_cup:
                break
            cups.append(current_cup.label + 1)
        return cups

    def make_move(self) -> None:
        picked_up, first, last = self.pick_up_three_cups()
        destination = (self.current_cup.label - 1) % self.max_cup
        while destination in picked_up:
            destination = (destination - 1) % self.max_cup
        self.insert_three_cups(first, last, destination)
        self.move_current()


def part_1(print_result: bool = True) -> int:
    circle = Circle(INITIAL_CIRCLE)
    for _ in range(100):
        circle.make_move()
    result = int("".join(str(c) for c in circle.from_first()))

    if print_result:
        print(f"Labels on cups after cup 1: {result}")
    return result


def part_2(print_result: bool = True) -> int:
    initial_circle = INITIAL_CIRCLE + tuple(range(10, 1_000_000 + 1))
    circle = Circle(initial_circle)
    for n in range(10):
        start_time = perf_counter_ns()
        for _ in range(1_000_000):
            circle.make_move()
        current_time = perf_counter_ns()
        if print_result:
            elapsed_time_ms = (current_time - start_time) / 1_000_000
            print(f"Processed (total {(n + 1) * 1_000_000} rounds) in {elapsed_time_ms} ms")
    result = math.prod(circle.from_first(2))

    if print_result:
        print(f"Product of the first two cups after cup 1: {result}")
    return result


SOLUTION_1 = 78569234
SOLUTION_2 = 565615814504
IS_SOLUTION_2_SLOW = False

if __name__ == "__main__":
    part_1()
    part_2()
