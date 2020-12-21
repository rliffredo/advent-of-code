import re
from collections import Counter
from typing import List

from common import read_data


class PasswordInfo:
    def __init__(self, line):
        _, min_, max_, self.letter, self.password, _ = re.split(r"(\d+)-(\d+) ([a-z]): (\w+)", line)
        self.min = int(min_)
        self.max = int(max_)

    def policy_1(self) -> bool:
        letters_count = Counter(self.password)
        return self.min <= letters_count[self.letter] <= self.max

    def policy_2(self) -> bool:
        def is_letter_at(pos: int) -> bool:
            pos -= 1  # toboga indexes are 1-based
            if pos >= len(self.password):
                return False
            return self.password[pos] == self.letter

        return is_letter_at(self.min) != is_letter_at(self.max)


def parse_data() -> List[PasswordInfo]:
    specs_and_password = read_data("02", True)
    return [PasswordInfo(line) for line in specs_and_password]


def count_valid(passwords: List[PasswordInfo], test) -> int:
    return [test(password) for password in passwords].count(True)


def part_1(print_result: bool = True) -> int:
    passwords = parse_data()
    valid_passwords = count_valid(passwords, PasswordInfo.policy_1)
    if print_result:
        print(f"Number of invalid passwords (approach 1): {valid_passwords}")
    return valid_passwords


def part_2(print_result: bool = True) -> int:
    passwords = parse_data()
    valid_passwords = count_valid(passwords, PasswordInfo.policy_2)
    if print_result:
        print(f"Number of invalid passwords (approach 2): {valid_passwords}")
    return valid_passwords


SOLUTION_1 = 410
SOLUTION_2 = 694

if __name__ == "__main__":
    part_1()
    part_2()
