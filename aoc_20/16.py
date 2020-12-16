import functools
import itertools
import math
import re
from typing import List, Set

from common import read_data


class Rule:
    def __init__(self, raw_rule: str):
        matches = re.search(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)", raw_rule).groups()
        self.name = matches[0]
        self.range_1 = int(matches[1]), int(matches[2])
        self.range_2 = int(matches[3]), int(matches[4])

    def is_valid_field(self, n: int):
        return (self.range_1[0] <= n <= self.range_1[1]) or (self.range_2[0] <= n <= self.range_2[1])

    def find_invalid_fields(self, ticket: List[int]) -> Set[int]:
        return {n for n in ticket if not self.is_valid_field(n)}

    def is_ticket_valid(self, ticket: List[int]) -> bool:
        return all(self.is_valid_field(n) for n in ticket)


def parse_ticket(raw_ticket: str) -> List[int]:
    return [int(n) for n in raw_ticket.split(',')]


def parse_data():
    raw_data = read_data("16", True)
    # Load in sections
    raw_ticket_rules = []
    raw_own_ticket = []
    raw_other_tickets = []
    sections = [raw_ticket_rules, raw_own_ticket, raw_other_tickets].__iter__()
    tgt = next(sections)
    for line in raw_data:
        if not line:
            tgt = next(sections)
        else:
            tgt.append(line)
    # parse each section
    ticket_rules = [Rule(rule) for rule in raw_ticket_rules]
    own_ticket = parse_ticket(raw_own_ticket[1])
    other_tickets = [parse_ticket(ticket) for ticket in raw_other_tickets[1:]]
    return ticket_rules, own_ticket, other_tickets


def part_1(print_result: bool = True) -> int:
    rules, _, nearby_tickets = parse_data()

    all_invalid_fields = [functools.reduce(lambda f, rule: f & rule.find_invalid_fields(ticket), rules, set(ticket))
                          for ticket in nearby_tickets]
    invalid_tickets = len(all_invalid_fields)
    ticket_error_rate = sum(itertools.chain.from_iterable(all_invalid_fields))

    if print_result:
        print(f"There are {invalid_tickets} invalid tickets with a {ticket_error_rate} error rate")
    return ticket_error_rate


def part_2(print_result: bool = True) -> int:
    rules, own_ticket, nearby_tickets = parse_data()
    valid_tickets = [ticket for ticket in nearby_tickets if any(rule.is_ticket_valid(ticket) for rule in rules)]

    field_names = {}
    available_fields = list(range(len(own_ticket)))
    available_rules = rules.copy()
    # For simplicity, assume that even if more than a rule can apply on a field
    # there is exactly one rule that applies only on that field.
    while available_fields:
        for rule in available_rules:
            possible_fields_for_rule = [n for n in available_fields
                                        if all(rule.is_valid_field(ticket[n]) for ticket in valid_tickets)]
            if len(possible_fields_for_rule) == 1:
                rule_field = possible_fields_for_rule[0]
                field_names[rule.name] = rule_field
                available_rules.remove(rule)
                available_fields.remove(rule_field)
                break

    departure_fields = [n for f, n in field_names.items() if f.startswith("departure")]
    result = math.prod(own_ticket[f] for f in departure_fields)

    if print_result:
        print(f"All departures: {result}")
    return result


SOLUTION_1 = 23036
SOLUTION_2 = 1909224687553

if __name__ == "__main__":
    part_1()
    part_2()
