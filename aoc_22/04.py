from more_itertools import grouper, ilen

from common import read_data


class Section:
    def __init__(self, section_tuple):
        self.start = int(section_tuple[0])
        self.end = int(section_tuple[1])

    def __repr__(self):
        return f'{self.start}-{self.end}'

    def overlaps(self, other: 'Section', op) -> bool:
        return op(other.start <= boundary <= other.end for boundary in (self.start, self.end))


def parse_data():
    return list(grouper(
        (Section(section.split('-'))
         for line in read_data('04', True)
         for section in line.split(',')
         if line),
        2
    ))


def overlap_checker(f):
    return lambda pair: pair[0].overlaps(pair[1], f) or pair[1].overlaps(pair[0], f)


def part_1() -> int:
    assignments = parse_data()
    return ilen(filter(overlap_checker(all), assignments))


def part_2() -> int:
    assignments = parse_data()
    return ilen(filter(overlap_checker(any), assignments))


SOLUTION_1 = 441
SOLUTION_2 = 861

if __name__ == '__main__':
    print(part_1())
    print(part_2())
