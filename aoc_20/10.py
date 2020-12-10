import functools
from collections import Counter
from typing import List

from common import read_data, pairwise


def parse_data() -> List[int]:
    raw_data = read_data("10", True)
    data = [int(line) for line in raw_data]
    data.append(max(data)+3)  # computer
    data.append(0)  # plug
    return data


def part_1():
    jolts = parse_data()
    jolt_steps = [j2 - j1 for j1, j2 in pairwise(sorted(jolts))]
    jolt_count = Counter(jolt_steps)
    print(f"There are {jolt_count[1]} 1-steps and {jolt_count[3]} 3-steps, "
          f"with checksum {jolt_count[1]*jolt_count[3]}")


def part_2():

    jolts = set(parse_data())
    target = max(jolts)

    @functools.lru_cache(maxsize=None)
    def count_combinations(root):
        if root not in jolts:
            return 0
        if root == target:
            return 1
        return sum(count_combinations(root+child) for child in (1, 2, 3))

    all_combinations = count_combinations(0)
    print(f"There are {all_combinations} possible combinations")


part_1()
part_2()
