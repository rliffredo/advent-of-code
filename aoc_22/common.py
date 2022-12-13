from typing import List, Union

from more_itertools import split_at


# noinspection DuplicatedCode
def read_data(day: str, by_lines: bool = False) -> Union[List[str], str]:
    file_name = f'data/{day}.txt'
    f = open(file_name)
    data = f.read()
    return data.split('\n') if by_lines else data


def read_line_groups(day: str) -> List[List[str]]:
    lines = read_data(day, True)
    return list(split_at(lines, lambda l: not l))


def distance(p1, p2):
    return abs(round(p1[0]) - round(p2[0])) + abs(round(p1[1]) - round(p2[1]))


# noinspection DuplicatedCode
def print_map(sizes, map_to_color, *, inverted_y=False):
    min_x, max_x, min_y, max_y = sizes
    lines = []
    for y in range(min_y, max_y+1):
        line = []
        for x in range(min_x, max_x+1):
            color = map_to_color(x, y)
            line.append(color)
        lines.append(''.join(line))
    if inverted_y:
        lines.reverse()
    for line in lines:
        print(line)


def make_map(sizes, map_to_color):
    lines = []
    min_x, max_x, min_y, max_y = sizes
    for y in range(min_y, max_y+1):
        line = []
        for x in range(min_x, max_x+1):
            color = map_to_color(x, y)
            line.append(color)
        lines.append(''.join(line))
    return '\n'.join(lines)
