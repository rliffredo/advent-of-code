from common import read_line_groups


def parse_data():
    elves_str = read_line_groups('01')
    elves_int = [map(int, e) for e in elves_str]
    return elves_int


def part_1() -> int:
    elves = parse_data()
    total_calories_per_elf = [sum(elf) for elf in elves]
    return max(total_calories_per_elf)


def part_2() -> int:
    elves = parse_data()
    total_calories_per_elf = [sum(elf) for elf in elves]
    most_calories = list(sorted(total_calories_per_elf))[-3:]
    return sum(most_calories)


SOLUTION_1 = 70374
SOLUTION_2 = 204610

if __name__ == '__main__':
    print(part_1())
    print(part_2())
