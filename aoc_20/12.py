import cmath
import math
from typing import List, TypeVar, Type

from common import read_data, distance


def rotate(p: complex, degrees: int) -> complex:
    radians = math.radians(degrees)
    r, phi = cmath.polar(p)
    return cmath.rect(r, phi + radians)


class MoveCommand:
    def __init__(self, line: str):
        self.command = line[0]
        amount = int(line[1:])
        # We move in "negative" direction for North, West and Left
        self.amount = -amount if self.command in "NWL" else amount


class MoveCommand1(MoveCommand):
    def __init__(self, line: str):
        super().__init__(line)
        if self.command in "NS":
            self.movement = lambda s, d: (s + complex(0, 1) * self.amount, d)
        elif self.command in "EW":
            self.movement = lambda s, d: (s + complex(1, 0) * self.amount, d)
        elif self.command in "LR":
            self.movement = lambda s, d: (s, rotate(d, self.amount))
        else:
            self.movement = lambda s, d: (s + d * self.amount, d)


CommandType = TypeVar('CommandType', bound=MoveCommand)


def parse_data(command_class: Type[CommandType]) -> List[CommandType]:
    raw_data = read_data("12", True)
    return [command_class(line) for line in raw_data]


def part_1(print_result: bool = True) -> int:
    commands = parse_data(MoveCommand1)
    # we use a vector for the direction
    position, direction = complex(0, 0), complex(1, 0)
    for command in commands:
        position, direction = command.movement(position, direction)

    d = distance((0, 0), (position.real, position.imag))
    if print_result:
        print(f"Ship moved by {d}")
    return d


class MoveCommand2(MoveCommand):
    def __init__(self, line: str):
        super().__init__(line)
        # Waypoint movement
        if self.command in "NS":
            self.movement = lambda s, w: (s, w + complex(0, 1) * self.amount)
        elif self.command in "EW":
            self.movement = lambda s, w: (s, w + complex(1, 0) * self.amount)
        elif self.command in "LR":
            self.movement = lambda s, w: (s, rotate(w, self.amount))
        else:
            self.movement = lambda s, w: (s + w * self.amount, w)


def part_2(print_result: bool = True) -> int:
    commands = parse_data(MoveCommand2)
    ship_position, waypoint_position = complex(0, 0), complex(10, -1)
    for command in commands:
        ship_position, waypoint_position = command.movement(ship_position, waypoint_position)
    d = distance((0, 0), (ship_position.real, ship_position.imag))
    if print_result:
        print(f"Ship moved by {d}")
    return d


SOLUTION_1 = 759
SOLUTION_2 = 45763

if __name__ == "__main__":
    part_1()
    part_2()
