from typing import List

from common import read_data


def parse_data() -> List[int]:
    raw_data = read_data("09", True)
    return [int(n) for n in raw_data]


class XmasBuffer:
    def __init__(self, priming: List[int]):
        self.buffer = []
        for i, n in enumerate(priming):
            all_pairs = [n + other_n for other_i, other_n in enumerate(priming) if i != other_i]
            self.buffer.append((n, all_pairs))

    def push(self, n: int) -> bool:
        for pair_sums in self.buffer:
            if n in pair_sums[1]:
                break
        else:
            return False
        del self.buffer[0]
        all_pairs = [n + other_val[0] for other_val in self.buffer]
        self.buffer.append((n, all_pairs))
        return True


def part_1(print_result: bool = True) -> int:
    numbers = parse_data()
    xmas_buffer = XmasBuffer(numbers[:25])
    for n in numbers[25:]:
        if not xmas_buffer.push(n):
            if print_result:
                print(f"Found invalid {n}")
            return n
    else:
        assert False, "There is at least one solution!"


def part_2(print_result: bool = True) -> int:
    numbers = parse_data()
    target = 14144619
    for i in range(len(numbers)):
        s = 0
        for j in range(i, len(numbers)):
            s += numbers[j]
            if s == target and j-i > 1:
                weakness = min(numbers[i:j]) + max(numbers[i:j])
                if print_result:
                    print(f"Found weakness {weakness} at range {i}-{j}")
                return weakness
            elif s > target:
                break


SOLUTION_1 = 14144619
SOLUTION_2 = 1766397

if __name__ == "__main__":
    part_1()
    part_2()
