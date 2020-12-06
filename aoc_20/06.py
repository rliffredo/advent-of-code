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


def part_1():
    group_answers = parse_data()
    print(f"Total number of positive answers (any) is {sum(g.number_any_positive for g in group_answers)}")


def part_2():
    group_answers = parse_data()
    print(f"Total number of positive answers (all) is {sum(g.number_all_positive for g in group_answers)}")


part_1()  # 6297
part_2()  # 3158
