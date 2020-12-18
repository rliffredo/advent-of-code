from abc import ABC
from typing import List, Tuple, Optional

from common import read_data


def parse_data() -> List[str]:
    raw_data = read_data("18", True)
    return [line for line in raw_data]


class Operation:
    ORDER = 1

    def evaluate(self) -> int:
        raise NotImplementedError()


class BinaryOperation(Operation, ABC):
    def __init__(self, left: Operation):
        assert left is not None
        self.left = left
        self.right: Optional[Operation] = None


class Number(Operation):
    def __init__(self, value: str):
        self.value = value

    def evaluate(self) -> int:
        return int(self.value)

    def __repr__(self):
        return self.value


class Group(Operation):
    def __init__(self, value: Operation):
        self.value = value

    def evaluate(self) -> int:
        return self.value.evaluate()

    def __repr__(self):
        return f'({self.value})'


class Sum(BinaryOperation):
    def evaluate(self) -> int:
        assert self.left and self.right
        return self.left.evaluate() + self.right.evaluate()

    def __repr__(self):
        return f'({self.left} + {self.right})'


class Prod(BinaryOperation):
    def evaluate(self) -> int:
        assert self.left and self.right
        return self.left.evaluate() * self.right.evaluate()

    def __repr__(self):
        return f'({self.left} * {self.right})'


def evaluate_expression(line: str) -> int:
    line = line.replace(' ', '')
    parsed_expression = parse_expression(line)[0]
    return parsed_expression.evaluate()


def parse_expression(line: str) -> Tuple[Operation, int]:
    current_position = 0
    current_op = None
    while current_position < len(line):
        char = line[current_position]
        if char.isnumeric():
            current_op = set_number(current_op, Number(char))
        elif char == '+':
            current_op = set_operation(current_op, Sum)
        elif char == '*':
            current_op = set_operation(current_op, Prod)
        elif char == '(':
            result, offset = parse_expression(line[current_position + 1:])
            current_position += offset + 1
            current_op = set_number(current_op, result)
        elif char == ')':
            break
        current_position += 1

    return Group(current_op), current_position


def set_operation(current_op, op_class):
    if current_op.ORDER > op_class.ORDER:
        current_op.right = op_class(current_op.right)
    else:
        current_op = op_class(current_op)
    return current_op


def set_number(current_op, result):
    if not current_op:
        return result

    op = current_op
    while op.right is not None:
        op = op.right
    op.right = result
    return current_op


def part_1(print_result: bool = True) -> int:
    result = sum(evaluate_expression(line) for line in parse_data())
    if print_result:
        print(f"Result 1 is {result}")
    return result


def part_2(print_result: bool = True) -> int:
    Prod.ORDER = 2
    result = sum(evaluate_expression(line) for line in parse_data())
    if print_result:
        print(f"Result 2 is {result}")
    return result


SOLUTION_1 = 5374004645253
SOLUTION_2 = 88782789402798

if __name__ == "__main__":
    part_1()
    part_2()
