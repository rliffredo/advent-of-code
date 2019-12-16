from itertools import tee, islice

try:
    from build import intcode
except ImportError:
    import intcode


def print_map(sizes, map_to_color):
    min_x, max_x, min_y, max_y = sizes
    for y in range(min_y, max_y+1):
        line = []
        for x in range(min_x, max_x+1):
            color = map_to_color(x, y)
            line.append(color)
        print(''.join(line))


def get_map_dimensions(map_2d):
    """
    Key is a tuple, and first two elements are (x, y)
    """
    min_x = min(map_2d.keys(), key=lambda p: p[0])[0]
    max_x = max(map_2d.keys(), key=lambda p: p[0])[0]
    min_y = min(map_2d.keys(), key=lambda p: p[1])[1]
    max_y = max(map_2d.keys(), key=lambda p: p[1])[1]
    return min_x, max_x, min_y, max_y


def read_data(day, by_lines=False):
    file_name = f'data/{day}.txt'
    f = open(file_name)
    return f.readlines() if by_lines else f.read()


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


######################
# Itertools recipes

def pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def take(n, iterable):
    """
    Return first n items of the iterable as a list
    """
    return list(islice(iterable, n))
