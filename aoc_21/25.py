from common import read_data, print_map


def parse_data():
    lines = read_data("25", True)
    cucumbers = {(x, y): char for y, line in enumerate(lines) for x, char in enumerate(line) if char != "."}
    return cucumbers, (len(lines[0]), len(lines))


def print_sea_bed(cucumbers, size):
    sizes = (0, size[0]-1, 0, size[1]-1)
    print_map(sizes, lambda x, y: cucumbers.get((x, y), "."))


def move_east(position, cucumbers, size):
    if cucumbers[position] != ">":
        return position
    x, y = position
    new_position = (x + 1) % size[0], y
    return position if new_position in cucumbers else new_position


def move_south(position, cucumbers, size):
    if cucumbers[position] != "v":
        return position
    x, y = position
    new_position = x, (y + 1) % size[1]
    return position if new_position in cucumbers else new_position


def move_cucumbers(cucumbers, size):
    cucumbers = {move_east(position, cucumbers, size): cucumber
                 for position, cucumber in cucumbers.items()}
    cucumbers = {move_south(position, cucumbers, size): cucumber
                 for position, cucumber in cucumbers.items()}
    return cucumbers


def part_1(print_result: bool = True) -> int:
    cucumbers, size = parse_data()
    current_step = 0
    if print_result:
        print("Initial state:")
        print_sea_bed(cucumbers, size)
    while True:
        current_step += 1
        moved_cucumbers = move_cucumbers(cucumbers, size)
        if moved_cucumbers == cucumbers:
            break
        cucumbers = moved_cucumbers
    if print_result:
        print(f"\nAfter {current_step} steps:")
        print_sea_bed(moved_cucumbers, size)
    return current_step


def part_2(print_result: bool = True) -> int:
    return 50


SOLUTION_1 = 337
SOLUTION_2 = 50


if __name__ == "__main__":
    print(part_1())
    print(part_2())
