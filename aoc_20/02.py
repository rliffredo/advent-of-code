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
    return sum(1 for password in passwords if test(password))


passwords = parse_data()
print(f"Number of invalid passwords (approach 1): {count_valid(passwords, PasswordInfo.policy_1)}")
print(f"Number of invalid passwords (approach 2): {count_valid(passwords, PasswordInfo.policy_2)}")
