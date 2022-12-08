from typing import List, Union


# noinspection DuplicatedCode
def read_data(day: str, by_lines: bool = False) -> Union[List[str], str]:
    file_name = f'data/{day}.txt'
    f = open(file_name)
    data = f.read()
    return data.split('\n') if by_lines else data


def read_line_groups(day: str) -> List[List[str]]:
    """
    Read lines, and groups them using empty lines as separator
    """
    lines = read_data(day, True)
    groups = []
    buffer_lines = []
    for line in lines:
        if line:
            buffer_lines.append(line)
        else:
            groups.append(buffer_lines)
            buffer_lines = []
    return groups


def distance(p1, p2):
    return abs(round(p1[0]) - round(p2[0])) + abs(round(p1[1]) - round(p2[1]))


# noinspection DuplicatedCode
def print_map(sizes, map_to_color):
    min_x, max_x, min_y, max_y = sizes
    for y in range(min_y, max_y+1):
        line = []
        for x in range(min_x, max_x+1):
            color = map_to_color(x, y)
            line.append(color)
        print(''.join(line))


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
