from typing import NamedTuple

from common import read_data, print_map


class Point(NamedTuple):
    x: int
    y: int

    def __repr__(self):
        return f'(x:{self.x}, y:{self.y})'


def parse_motions():
    moves = {
        'U': (0, 1), 'D': (0, -1),
        'R': (1, 0), 'L': (-1, 0),
    }
    return [
        (moves[line.split()[0]], int(line.split()[1]))
        for line in read_data("09", True)
        if line
    ]


def move_knot(head, offset):
    return Point(head.x + offset[0], head.y + offset[1])


def follow_tail(head, tail):
    while abs(head.x - tail.x) > 1 or abs(head.y - tail.y) > 1:
        if head.x > tail.x:
            tail = move_knot(tail, (1, 0))
        elif head.x < tail.x:
            tail = move_knot(tail, (-1, 0))
        if head.y > tail.y:
            tail = move_knot(tail, (0, 1))
        elif head.y < tail.y:
            tail = move_knot(tail, (0, -1))
    return tail


def record_tail_movements(motions, rope, print_steps):
    tails = {rope[-1]}
    for motion in motions:
        for _ in range(motion[1]):
            rope[0] = move_knot(rope[0], motion[0])
            for knot_position in range(1, len(rope)):
                rope[knot_position] = follow_tail(rope[knot_position - 1], rope[knot_position])
            tails.add(rope[-1])
        if print_steps:
            print_rope(rope)
    return tails


def print_rope(rope):
    def print_point(x, y):
        p = Point(x, y)
        if p in rope:
            return 'H' if p == rope[0] else 'T' if p == rope[-1] else str(rope.index(p))
        return 's' if (x, y) == (0, 0) else '.'

    map_sizes = (
        min(0, min(k.x for k in rope)), max(0, max(k.x for k in rope)) + 1,
        min(0, min(k.y for k in rope)), max(0, max(k.y for k in rope)) + 1,
    )
    print(f'Current rope: {rope}')
    print_map(map_sizes, print_point, inverted_y=True)


def part_1(print_result: bool = True) -> int:
    motions = parse_motions()
    rope = [Point(0, 0) for _ in range(2)]
    tails = record_tail_movements(motions, rope, print_result)
    return len(tails)


def part_2(print_result: bool = True) -> int:
    motions = parse_motions()
    rope = [Point(0, 0) for _ in range(10)]
    tails = record_tail_movements(motions, rope, print_result)
    return len(tails)


SOLUTION_1 = 5735
SOLUTION_2 = 2478

if __name__ == "__main__":
    print(part_1())
    print(part_2())
