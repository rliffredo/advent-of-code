from common import read_data


def parse_data():
    lines = read_data("01", True)
    elves = []
    current_elf = []
    for line in lines:
        if not line:
            elves.append(current_elf)
            current_elf = []
        else:
            current_elf.append(int(line))
    if current_elf:
        elves.append(current_elf)
    return elves


def part_1(print_result: bool = True) -> int:
    elves = parse_data()
    total_calories_per_elf = [sum(elf) for elf in elves]
    return max(total_calories_per_elf)


def part_2(print_result: bool = True) -> int:
    elves = parse_data()
    total_calories_per_elf = [sum(elf) for elf in elves]
    most_calories = list(sorted(total_calories_per_elf))[-3:]
    print(most_calories)
    return sum(most_calories)


SOLUTION_1 = -1
SOLUTION_2 = -1

if __name__ == "__main__":
    print(part_1())
    print(part_2())

