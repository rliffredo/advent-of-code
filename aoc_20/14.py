from typing import List, Tuple, Optional, Union

from common import read_data


Command = Tuple[str, Union[int, str], Optional[int]]


def parse_data() -> List[Command]:
    def parse_line(line):
        command, param = line.split(" = ")
        if command.startswith("mem"):
            return "set_number", int(param), int(command.split('[')[1][:-1])
        else:
            return "set_mask", param, None

    raw_data = read_data("14", True)
    return [parse_line(line) for line in raw_data]


class DockProcessorV1:
    def __init__(self):
        self.memory = {}
        self.mask_and = 0
        self.mask_or = 0

    def set_mask(self, _, mask_string: str) -> None:
        bit = 1
        self.mask_and = 0
        self.mask_or = 0
        for bit_value in reversed(mask_string):
            self.mask_and += bit if bit_value in 'X1' else 0
            self.mask_or += bit if bit_value in '1' else 0
            bit *= 2

    def set_number(self, address: int, value: int) -> None:
        masked_value = (value | self.mask_or) & self.mask_and
        self.memory[address] = masked_value


def part_1(print_result: bool = True) -> int:
    dock_vm = DockProcessorV1()
    for command, param1, param2 in parse_data():
        operation = getattr(dock_vm, command)
        operation(param2, param1)
    result = sum(dock_vm.memory.values())
    if print_result:
        print(f"Memory sum is {result}")
    return result


class DockProcessorV2:
    def __init__(self):
        self.memory = {}
        self.mask_and = []
        self.mask_or = 0

    def set_mask(self, _, mask_string: str) -> None:
        bit = 1
        self.mask_and = [0]
        self.mask_or = 0
        for bit_value in reversed(mask_string):
            self.mask_or = self.mask_or + (bit if bit_value in 'X1' else 0)
            self.mask_and = (self.mask_and if bit_value == 'X' else []) + [mask+bit for mask in self.mask_and]
            bit *= 2

    def set_number(self, address: int, value: int) -> None:
        memory_addresses = [(address | self.mask_or) & mask for mask in self.mask_and]
        for memory_address in memory_addresses:
            self.memory[memory_address] = value


def part_2(print_result: bool = True) -> int:
    dock_vm = DockProcessorV2()
    for command, param1, param2 in parse_data():
        operation = getattr(dock_vm, command)
        operation(param2, param1)
    result = sum(dock_vm.memory.values())
    if print_result:
        print(f"Memory sum is {result}")
    return result


SOLUTION_1 = 10717676595607
SOLUTION_2 = 3974538275659

if __name__ == "__main__":
    part_1()
    part_2()
