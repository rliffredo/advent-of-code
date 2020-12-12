from itertools import tee
from typing import List, Union


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


######################
# Itertools recipes

def pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
