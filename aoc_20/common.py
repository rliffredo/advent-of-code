from itertools import tee


def read_data(day, by_lines=False):
    file_name = f'data/{day}.txt'
    f = open(file_name)
    data = f.read()
    return data.split('\n') if by_lines else data


######################
# Itertools recipes

def pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
