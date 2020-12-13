from typing import List

from common import read_line_groups


class GroupAnswers(object):
    def __init__(self, group_line: List[str]):
        self._any_positive_answers = set()
        self._all_positive_answers = set("abcdefghijklmnopqrstuvwxyz")
        for line in group_line:
            self.add_answer(line)

    def add_answer(self, form: str):
        self._any_positive_answers.update(form)
        self._all_positive_answers.intersection_update(form)

    @property
    def number_any_positive(self) -> int:
        return len(self._any_positive_answers)

    @property
    def number_all_positive(self) -> int:
        return len(self._all_positive_answers)


def parse_data():
    grouped_lines = read_line_groups("06")
    return [GroupAnswers(group_answers) for group_answers in grouped_lines]


def part_1(print_result: bool = True) -> int:
    group_answers = parse_data()
    positive_answers = sum(g.number_any_positive for g in group_answers)
    if print_result:
        print(f"Total number of positive answers (any) is {positive_answers}")
    return positive_answers


def part_2(print_result: bool = True) -> int:
    group_answers = parse_data()
    positive_answers = sum(g.number_all_positive for g in group_answers)
    if print_result:
        print(f"Total number of positive answers (all) is {positive_answers}")
    return positive_answers


SOLUTION_1 = 6297
SOLUTION_2 = 3158

if __name__ == "__main__":
    part_1()
    part_2()
