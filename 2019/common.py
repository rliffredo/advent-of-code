from itertools import tee


def read_data(day, by_lines=False):
    file_name = f'data/{day}.txt'
    f = open(file_name)
    return f.readlines() if by_lines else f.read()


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
