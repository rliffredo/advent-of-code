from more_itertools import grouper, ilen

from common import read_data


class Section:
    def __init__(self, section_tuple):
        self.start = int(section_tuple[0])
        self.end = int(section_tuple[1])

    def __repr__(self):
        return f'{self.start}-{self.end}'

    def is_inside(self, other: 'Section') -> bool:
        return (other.start <= self.start <= other.end) and (other.start <= self.end <= other.end)

    def overlaps(self, other: 'Section') -> bool:
        return (other.start <= self.start <= other.end) or (other.start <= self.end <= other.end)


def parse_data():
    return list(grouper(
        (Section(section.split('-'))
         for line in read_data("04", True)
         for section in line.split(',')
         if line),
        2
    ))


def checker(f):
    return lambda pair: f(pair[0], pair[1]) or f(pair[1], (pair[0]))


def part_1(print_result: bool = True) -> int:
    assignments = parse_data()
    return ilen(filter(checker(Section.is_inside), assignments))


def part_2(print_result: bool = True) -> int:
    assignments = parse_data()
    return ilen(filter(checker(Section.overlaps), assignments))


SOLUTION_1 = 441
SOLUTION_2 = 861

if __name__ == "__main__":
    print(part_1())
    print(part_2())
