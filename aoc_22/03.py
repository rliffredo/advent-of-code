from more_itertools import grouper

from common import read_data


def parse_data():
    return [l for l in read_data("03", True) if l]


def item_priority(item: str):
    prio = ord(item)
    return prio - 96 if prio > 90 else prio - 64 + 26


def sum_priority_items_in_common(rucksack_grouper):
    rucksacks = parse_data()
    grouped_rucksacks = rucksack_grouper(rucksacks)
    common_items = [set.intersection(*r).pop() for r in grouped_rucksacks]
    priorities = [item_priority(c) for c in common_items]
    return sum(priorities)


def part_1(print_result: bool = True) -> int:
    def group_rucksacks_by_bag(rucksacks):
        split_rucksacks = [(r[:len(r) // 2], r[len(r) // 2:]) for r in rucksacks]
        unique_rucksacks = [(set(r[0]), set(r[1])) for r in split_rucksacks]
        return unique_rucksacks

    return sum_priority_items_in_common(group_rucksacks_by_bag)


def part_2(print_result: bool = True) -> int:
    def group_rucksacks_by_team(rucksacks):
        unique_rucksacks = [set(r) for r in rucksacks]
        rucksacks_in_groups = grouper(unique_rucksacks, 3)
        return rucksacks_in_groups

    return sum_priority_items_in_common(group_rucksacks_by_team)


SOLUTION_1 = 8202
SOLUTION_2 = 2864

if __name__ == "__main__":
    print(part_1())
    print(part_2())
