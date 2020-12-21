import re
from functools import lru_cache
from typing import List, Tuple, Dict

from common import read_data


def make_rule(line: str) -> Tuple[str, Tuple[str, ...]]:
    rule_id, rule_raw = line.split(': ')
    rule = tuple(rule_raw.strip(' "').split())
    return rule_id, rule


def compile_rule(rule_id: int, rules: Dict[str, Tuple[str, ...]], recursive_rules: Tuple[str, ...] = ()) -> re.Pattern:
    @lru_cache(maxsize=2000)  # Note that the gain given by the cache here is minimal, around 5%
    def transform_rule(rule: str, depth=0) -> List[str]:
        rule_parts = rules[rule]
        new_rules = ['(']
        for part in rule_parts:
            if part.isnumeric():
                if part in recursive_rules:
                    depth += 1
                if depth > 5:
                    continue
                new_rules.extend(transform_rule(part, depth))
            else:
                new_rules.append(part)
        new_rules.append(')')
        # Most of the time is actually spent on compiling the regular expression.
        # Small simplification of regular expression, can lead to a significant
        return new_rules if len(new_rules) > 3 else new_rules[1]

    transformed_rule = "".join(transform_rule(str(rule_id)))
    compiled_rule = re.compile(transformed_rule)
    return compiled_rule


def parse_data() -> Tuple[Dict[str, Tuple[str, ...]], List[str]]:
    raw_rules, raw_messages = read_data("19", False).split("\n\n")
    rules = dict(make_rule(line) for line in raw_rules.split("\n"))
    messages = [line for line in raw_messages.split("\n")]
    return rules, messages


def part_1(print_result: bool = True) -> int:
    raw_rules, messages = parse_data()
    rule = compile_rule(0, raw_rules)
    total_matching_messages = len(messages) - [rule.fullmatch(message) for message in messages].count(None)

    if print_result:
        print(f"A total of {total_matching_messages} messages match rule 0")
    return total_matching_messages


def part_2(print_result: bool = True) -> int:
    raw_rules, messages = parse_data()
    rules_update = {
        "8": ("42", "|", "42", "8"),
        "11": ("42", "31", "|", "42", "11", "31"),
    }
    raw_rules.update(rules_update)
    rule = compile_rule(0, raw_rules, tuple(rules_update.keys()))
    total_matching_messages = len(messages) - [rule.fullmatch(message) for message in messages].count(None)

    if print_result:
        print(f"A total of {total_matching_messages} messages match rule 0 (after update)")
    return total_matching_messages


SOLUTION_1 = 132
SOLUTION_2 = 306

if __name__ == "__main__":
    part_1()
    part_2()
