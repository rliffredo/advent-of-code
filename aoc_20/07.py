import re
from typing import Set, Mapping

from common import read_data


class BagRule:
    CONTAINED = re.compile(r" bags?[,.] ?")
    DETAILED_INFO = re.compile(r"(\d+) (.*)")

    def __init__(self, raw_rule):
        self.bag_color, contained_bags = raw_rule.split(" bags contain ")
        # parse contained bags
        contained = self.CONTAINED.split(contained_bags)
        split_contained = [self.DETAILED_INFO.findall(bag_info) for bag_info in contained]
        self.contained_bags = {split_info[0][1]: int(split_info[0][0]) for split_info in split_contained if split_info}

    def can_contain(self, inner_bag_colors: Set[str]) -> bool:
        return any(bag_color in self.contained_bags for bag_color in inner_bag_colors)


def parse_data() -> Mapping[str, BagRule]:
    raw_rules = read_data("07", True)
    rules = [BagRule(raw_rule) for raw_rule in raw_rules]
    return {rule.bag_color: rule for rule in rules}


def part_1():
    rules = parse_data()
    possible_bags = set()
    possible_inner = {"shiny gold"}
    while True:
        new_possible_bags = {rule.bag_color for rule in rules.values() if rule.can_contain(possible_inner)}
        if new_possible_bags == possible_bags:
            break
        possible_bags = new_possible_bags
        possible_inner.update(new_possible_bags)

    print(f"Total number of possible colors that contain shiny gold is {len(possible_bags)}")  # 274


def part_2():
    rules = parse_data()

    def count_bags(color: str) -> int:
        inner_bags = rules[color].contained_bags.items()
        return 1 + sum(inner_quantity * count_bags(inner_color) for inner_color, inner_quantity in inner_bags)

    total_bags = count_bags("shiny gold") - 1  # we already have "shiny gold"!
    print(f"Total number of bags to buy is {total_bags}")  # 158730


part_1()
part_2()
