import math
import re

from common import read_data


class Monkey:
    def __init__(self, monkey_id, decrease_worry_level):
        self.monkey_id = monkey_id
        self.decrease_worry_level = decrease_worry_level
        self.items = []
        self.operation_params = None
        self.test_params = [-1, -1, -1]
        self.items_inspected = 0
        self.decrease_factor = 3 if decrease_worry_level else 1
        self.total_modulo = 1

    def throw_items(self, monkeys: list['Monkey']) -> None:
        for item in self.items:
            # Fun factoid: using methods here will increase execution time in
            # part 2 by 10-15ms for each function
            worry_level = self._new_worry_level(item)
            destination = self._next_monkey(worry_level)
            monkeys[destination].items.append(worry_level)
        self.items_inspected += len(self.items)
        self.items = []

    def _new_worry_level(self, old_worry_level: int) -> int:
        left = old_worry_level if self.operation_params[0] == 'old' else int(self.operation_params[0])
        right = old_worry_level if self.operation_params[2] == 'old' else int(self.operation_params[2])
        increased_worry_level = (left * right) if self.operation_params[1] == '*' else (left + right)
        decreased_worry_level = increased_worry_level // self.decrease_factor
        return decreased_worry_level % self.total_modulo

    def _next_monkey(self, worry_level: int) -> int:
        is_divisible = worry_level % self.test_params[0] == 0
        new_monkey = self.test_params[1] if is_divisible else self.test_params[2]
        return new_monkey


def parse_data(decrease_worry_level):
    monkeys = []
    current_monkey = None
    for line in read_data("11", True):
        match re.split(r'[ :]', line.strip()):
            case ['']:
                if current_monkey:
                    monkeys.append(current_monkey)
                    current_monkey = None
            case ['Monkey', monkey_id, '']:
                assert not current_monkey
                current_monkey = Monkey(monkey_id, decrease_worry_level)
            case ['Starting', 'items', '', *starting_items]:
                current_monkey.items = [int(item.strip(',')) for item in starting_items]
            case ['Operation', *_, left, op, right]:
                current_monkey.operation_params = [left, op, right]
            case ['Test', *_, divisible_by]:
                current_monkey.test_params[0] = int(divisible_by)
            case ['If', condition, *_, monkey_id]:
                current_monkey.test_params[1 if condition == 'true' else 2] = int(monkey_id)
    if current_monkey:
        monkeys.append(current_monkey)
    # keep numbers down, because all tests are about modulo, so we can just
    # limit the global space
    for m in monkeys:
        m.total_modulo = math.prod(m.test_params[0] for m in monkeys)
    return monkeys


def calc_monkey_business_level(monkeys, iterations):
    for _ in range(iterations):
        for monkey in monkeys:
            monkey.throw_items(monkeys)
    return math.prod(sorted(m.items_inspected for m in monkeys)[-2:])


def part_1(print_result: bool = True) -> int:
    monkeys = parse_data(decrease_worry_level=True)
    return calc_monkey_business_level(monkeys, iterations=20)


def part_2(print_result: bool = True) -> int:
    monkeys = parse_data(decrease_worry_level=False)
    return calc_monkey_business_level(monkeys, iterations=10000)


SOLUTION_1 = 78960
SOLUTION_2 = 14561971968

if __name__ == "__main__":
    print(part_1())
    print(part_2())
